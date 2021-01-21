#!/usr/bin/env python3
#
#  __init__.py
"""
Search the Python documentation from your terminal.
"""
#
#  Copyright © 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import functools
import shutil
from base64 import urlsafe_b64encode
from typing import Union

# 3rd party
import appdirs  # type: ignore
import diskcache  # type: ignore
import sphobjinv  # type: ignore
from apeye import URL, RequestsURL
from domdf_python_tools.paths import PathPlus

__all__ = [
		"cache_dir",
		"resolve_url",
		"cache_dir_for_url",
		"download_objects_inv",
		"find_url",
		]

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2021 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.0.0"
__email__: str = "dominic@davis-foster.co.uk"

#: Directory in which cached files are stored.
cache_dir = PathPlus(appdirs.user_cache_dir("searchdocs"))
cache_dir.maybe_make(parents=True)


def resolve_url(url: Union[str, RequestsURL]) -> RequestsURL:
	"""
	Resolve any redirects in the given URL.

	:param url:
	"""

	return RequestsURL(RequestsURL(url).head().url)


@functools.lru_cache()
def cache_dir_for_url(url: Union[str, URL]) -> PathPlus:
	"""
	Returns the path to the cache subdirectory for the given URL.

	:param url:
	"""

	return cache_dir / urlsafe_b64encode(str(url).encode("UTF-8")).decode("UTF-8")


def download_objects_inv(docs_url: Union[str, RequestsURL]) -> PathPlus:
	"""
	Download the Sphinx ``objects.inv`` file for the documentation available at the given URL.

	:param docs_url: The base URL for the documentation, e.g. ``"https://docs.python.org/3/"``.

	:returns: The filename of the cached file.
	"""

	docs_url = resolve_url(docs_url)
	objects_inv_url = docs_url / "objects.inv"

	docs_cache_dir = cache_dir_for_url(docs_url)

	if docs_cache_dir.exists():
		current_etag = objects_inv_url.head().headers["etag"].strip('"')

		if (docs_cache_dir / current_etag).is_file():
			return docs_cache_dir / current_etag
		else:
			shutil.rmtree(docs_cache_dir)

	response = objects_inv_url.get()
	objects_inv_file = docs_cache_dir / response.headers["etag"].strip('"')
	objects_inv_file.parent.maybe_make(parents=True)
	objects_inv_file.write_bytes(response.content)

	return objects_inv_file


def find_url(docs_url: Union[str, RequestsURL], search_term: str) -> URL:
	"""
	Find the complete documentation URL for the given function, class, method etc.

	:param docs_url: The base URL for the documentation, e.g. ``"https://docs.python.org/3/"``.
	:param search_term: The object to search for, e.g. ``'TemporaryDirectory'``.

	:return: The url of the object in the documentation, e.g.
		``URL('https://docs.python.org/3/'library/tempfile.html#tempfile.TemporaryDirectory')``.
	"""

	docs_url = resolve_url(docs_url)
	docs_cache_dir = cache_dir_for_url(docs_url)

	objects_inv = download_objects_inv(docs_url)

	with diskcache.Cache(directory=str(docs_cache_dir)) as search_result_cache:
		if search_term in search_result_cache:
			return URL(search_result_cache[search_term])

		else:
			inventory = sphobjinv.inventory.Inventory(objects_inv)

			# TODO: expose with_score as an option?
			# TODO: match case
			suggestions = inventory.suggest(search_term, with_index=True)
			if not suggestions:
				raise ValueError(f"Object {search_term} not found.")

			desired_object = inventory.objects[suggestions[0][1]]
			url = docs_url / desired_object.uri_expanded

			search_result_cache.set(search_term, str(url))

			return url
