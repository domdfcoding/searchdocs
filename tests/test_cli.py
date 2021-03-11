# 3rd party
import pytest
from apeye import URL
from consolekit.testing import CliRunner, Result

# this package
from searchdocs.__main__ import main


def param(term: str, url: str):
	return pytest.param(term, URL(url), id=term)


@pytest.mark.parametrize(
		"term, url",
		[
				param("pathlib.Path", "https://docs.python.org/3/library/pathlib.html#pathlib.Path"),
				param("dict", "https://docs.python.org/3/library/stdtypes.html#dict"),
				param("dict ", "https://docs.python.org/3/library/stdtypes.html#dict"),
				param("dic", "https://docs.python.org/3/library/stdtypes.html#dict"),
				param("list", "https://docs.python.org/3/library/stdtypes.html#list"),
				param("list ", "https://docs.python.org/3/library/stdtypes.html#list"),
				param("Dict", "https://docs.python.org/3/library/stdtypes.html#dict"),
				param("set", "https://docs.python.org/3/library/stdtypes.html#set"),
				param("Set", "https://docs.python.org/3/library/stdtypes.html#set"),
				param(
						"difflib.get_clos_matches",
						"https://docs.python.org/3/library/difflib.html#difflib.get_close_matches"
						),
				param(
						"difflib.get_close_matches",
						"https://docs.python.org/3/library/difflib.html#difflib.get_close_matches"
						),
				param(
						"difflib.get_closest_matches",
						"https://docs.python.org/3/library/difflib.html#difflib.get_close_matches"
						),
				param("typing.Dict", "https://docs.python.org/3/library/typing.html#typing.Dict"),
				param("Dict ", "https://docs.python.org/3/library/stdtypes.html#dict"),
				param("NotImplemented", "https://docs.python.org/3/library/constants.html#NotImplemented"),
				param("False", "https://docs.python.org/3/library/constants.html#False"),
				param("True", "https://docs.python.org/3/library/constants.html#True"),
				param("None", "https://docs.python.org/3/library/constants.html#None"),
				param("sum", "https://docs.python.org/3/library/functions.html#sum"),
				param("staticmethod", "https://docs.python.org/3/library/functions.html#staticmethod"),
				param("license", "https://docs.python.org/3/library/constants.html#license"),
				param("Decimal", "https://docs.python.org/3/library/decimal.html#module-decimal"),
				param("decimal.Decimal", "https://docs.python.org/3/library/decimal.html#decimal.Decimal"),
				]
		)
def test_find_url(term: str, url: URL):

	runner = CliRunner()
	result: Result = runner.invoke(
			main,
			catch_exceptions=False,
			args=[term],
			)

	assert result.exit_code == 0
	assert result.stdout.strip() == str(url)


@pytest.mark.parametrize(
		"term",
		[
				"ArithmeticError",
				"AttributeError",
				"BrokenPipeError",
				"ConnectionRefusedError",
				"ConnectionResetError",
				"Exception",
				"FileExistsError",
				"GeneratorExit",
				"IOError",
				"ImportError",
				"IndexError",
				"InterruptedError",
				"IsADirectoryError",
				"KeyError",
				"MemoryError",
				"NotADirectoryError",
				"PendingDeprecationWarning",
				"PermissionError",
				"ResourceWarning",
				"RuntimeWarning",
				"StopAsyncIteration",
				"SyntaxError",
				"SystemError",
				"SystemExit",
				"TabError",
				"TimeoutError",
				"UnicodeTranslateError",
				"UserWarning",
				"ValueError",
				"Warning",
				]
		)
def test_find_url_exceptions(term: str):

	runner = CliRunner()
	result: Result = runner.invoke(
			main,
			catch_exceptions=False,
			args=[term],
			)

	assert result.exit_code == 0
	assert result.stdout.strip() == f"https://docs.python.org/3/library/exceptions.html#{term}"
