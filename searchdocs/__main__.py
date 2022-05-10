#!/usr/bin/env python3
#
#  __main__.py
"""
CLI entry point.
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
import sys

# 3rd party
import click
from apeye.requests_url import RequestsURL
from consolekit import click_command
from consolekit.commands import MarkdownHelpCommand
from consolekit.options import flag_option

__all__ = ["main"]

DOCS_PYTHON_ORG = RequestsURL("https://docs.python.org/3/")


@flag_option("--browser", help="Open the documentation in the default web browser.")
@click.argument("search_term", type=click.STRING)
@click_command(cls=MarkdownHelpCommand)
def main(search_term: str, browser: bool = False) -> None:
	"""
	Search for ``SEARCH_TERM`` in the Python documentation, and print the URL of the best match.
	"""

	# this package
	from searchdocs import find_url

	url = find_url(DOCS_PYTHON_ORG, search_term)

	if browser:  # pragma: no cover
		# stdlib
		import webbrowser

		webbrowser.open_new_tab(str(url))

	else:
		click.echo(url)


if __name__ == "__main__":
	sys.exit(main())
