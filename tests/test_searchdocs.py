# stdlib
import shutil

# 3rd party
import appdirs
import pytest
from apeye import URL
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike

# this package
from searchdocs import cache_dir_for_url, download_objects_inv, resolve_url
from searchdocs.__main__ import DOCS_PYTHON_ORG


def param(term: str, url: str):
	return pytest.param(term, URL(url), id=term)


def test_download_objects_inv():
	shutil.rmtree(cache_dir_for_url(DOCS_PYTHON_ORG), ignore_errors=True)
	download_objects_inv(DOCS_PYTHON_ORG)
	download_objects_inv(DOCS_PYTHON_ORG)


@pytest.mark.parametrize(
		"url, expected",
		[
				param("https://docs.python.org/", "https://docs.python.org/3/"),
				param(
						"https://domdf_python_tools.readthedocs.io/",
						"https://domdf-python-tools.readthedocs.io/en/latest/"
						),
				]
		)
def test_resolve_url(url: str, expected: URL):
	assert str(resolve_url(url)) == str(expected)
	assert resolve_url(url).strict_compare(expected)


@pytest.mark.parametrize(
		"url, expected",
		[
				("https://docs.python.org/", "aHR0cHM6Ly9kb2NzLnB5dGhvbi5vcmcv"),
				(
						"https://domdf_python_tools.readthedocs.io/",
						"aHR0cHM6Ly9kb21kZl9weXRob25fdG9vbHMucmVhZHRoZWRvY3MuaW8v"
						),
				]
		)
def test_cache_dir_for_url(url: str, expected: PathLike):
	expected = PathPlus(appdirs.user_cache_dir("searchdocs")) / expected

	assert cache_dir_for_url(url) == expected
