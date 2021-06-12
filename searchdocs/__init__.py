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
import re
import shutil
import warnings
from base64 import urlsafe_b64encode
from typing import List, Tuple, Union, overload

# 3rd party
import appdirs
import diskcache  # type: ignore
import sphobjinv  # type: ignore
from apeye import URL
from apeye.requests_url import RequestsURL
from domdf_python_tools.paths import PathPlus
from fuzzywuzzy.fuzz import ratio  # type: ignore
from typing_extensions import Literal

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
__version__: str = "0.2.0"
__email__: str = "dominic@davis-foster.co.uk"

#: Directory in which cached files are stored.
cache_dir = PathPlus(appdirs.user_cache_dir("searchdocs"))
cache_dir.maybe_make(parents=True)


def resolve_url(url: Union[str, RequestsURL]) -> RequestsURL:
	"""
	Resolve any redirects in the given URL.

	:param url:
	"""

	return RequestsURL(RequestsURL(url).head(allow_redirects=True).url)


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
		current_etag = objects_inv_url.head(allow_redirects=True).headers["etag"].strip('"')

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
			inventory = Inventory(objects_inv)

			# TODO: expose with_score as an option?
			suggestions: List[Tuple[str, int, int]] = inventory.suggest_from_name(
					search_term,
					with_index=True,
					with_score=True,
					)

			if not suggestions:
				raise ValueError(f"Object {search_term} not found.")

			desired_object = inventory.objects[suggestions[0][2]]
			url = docs_url / desired_object.uri_expanded

			search_result_cache.set(search_term, str(url))

			return url


class Inventory(sphobjinv.inventory.Inventory):

	# Based on https://github.com/bskinn/sphobjinv
	# Copyright (c) 2016-2021 Brian Skinn
	# MIT Licensed

	@overload
	def suggest_from_name(
			self,
			name: str,
			*,
			with_index: Literal[True],
			thresh: int = ...,
			with_score: Literal[False] = ...
			) -> List[Tuple[str, int]]: ...

	@overload
	def suggest_from_name(
			self,
			name: str,
			*,
			with_score: Literal[True],
			thresh: int = ...,
			with_index: Literal[False] = ...
			) -> List[Tuple[str, int]]: ...

	@overload
	def suggest_from_name(
			self,
			name: str,
			*,
			with_index: Literal[True],
			with_score: Literal[True],
			thresh: int = ...
			) -> List[Tuple[str, int, int]]: ...

	@overload
	def suggest_from_name(
			self,
			name: str,
			*,
			thresh: int = ...,
			with_index: Literal[False] = ...,
			with_score: Literal[False] = ...
			) -> List[str]: ...

	def suggest_from_name(
			self,
			name: str,
			*,
			thresh: int = 50,
			with_index: bool = False,
			with_score: bool = False
			) -> Union[List[str], List[Tuple[str, int]], List[Tuple[str, int, int]]]:
		"""
		Similar to :meth:`sphobjinv.inventory.Inventory.suggest`, but only searches the names of objects and not their types.

		:param name: Object name to search for.
		:param thresh: Match quality threshold
		:param with_index: Whether to include the index in the inventory of each match.
		:param with_score: Whether to include the match quality score for each matched name.

		| If both ``with_index`` and ``with_score`` are :py:obj:`True`, returns a list of 3-element tuples of ``(name, score, index)``.
		| If ``with_index`` is :py:obj:`True`, returns a list of 2-element tuples of ``(name, index)``.
		| If ``with_score`` is :py:obj:`True`, returns a list of 2-element tuples of ``(name, score)``.
		| If neither are :py:obj:`True`, returns a list of strings containing just the names.
		"""

		# Suppress any UserWarning about the speed issue
		with warnings.catch_warnings():
			warnings.simplefilter("ignore")
			# 3rd party
			from fuzzywuzzy import process as fwp  # type: ignore

		# Must propagate list index to include in output
		# Search vals are rst prepended with list index
		srch_list = [f"{i} {o}" for i, o in enumerate([_.name for _ in self.objects])]

		#
		# if name in srch_list:
		# 	if with_index and with_score:
		# 		return [(name, 100, srch_list.index(name))]
		# 	elif with_index:
		# 		return (name, srch_list.index(name))
		# 	elif with_score:
		# 		return (name, 100)
		# 	else:
		# 		return name

		# Composite each string result extracted by fuzzywuzzy
		# and its match score into a single string. The match
		# and score are returned together in a tuple.
		initial_results = [
				"{} {}".format(*_)
				for _ in fwp.extract(name, srch_list, limit=None, scorer=ratio)
				if _[1] >= thresh
				]

		# Define regex for splitting the three components, and
		# use it to convert composite result string to tuple:
		# result --> (rst, score, index)
		p_idx = re.compile("^(\\d+)\\s+(.+?)\\s+(\\d+)$")
		results = [
				(m.group(2), int(m.group(3)), int(m.group(1)))  # type: ignore
				for m in map(p_idx.match, initial_results)
				]

		# Return based on flags
		if with_score:
			if with_index:
				return results
			else:
				return [tup[:2] for tup in results]
		else:
			if with_index:
				return [tup[::2] for tup in results]
			else:
				return [tup[0] for tup in results]
