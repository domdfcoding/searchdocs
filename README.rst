###########
searchdocs
###########

.. start short_desc

**Search the Python documentation from your terminal.**

.. end short_desc

Built on top of `sphobjinv <https://sphobjinv.readthedocs.io/en/stable/>`_,
which can be used for more advanced manipulation and searching of Sphinx ``objects.inv`` files.

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/searchdocs/latest?logo=read-the-docs
	:target: https://searchdocs.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/searchdocs/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/searchdocs/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/domdfcoding/searchdocs/workflows/Linux/badge.svg
	:target: https://github.com/domdfcoding/searchdocs/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/searchdocs/workflows/Windows/badge.svg
	:target: https://github.com/domdfcoding/searchdocs/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/searchdocs/workflows/macOS/badge.svg
	:target: https://github.com/domdfcoding/searchdocs/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/domdfcoding/searchdocs/workflows/Flake8/badge.svg
	:target: https://github.com/domdfcoding/searchdocs/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/domdfcoding/searchdocs/workflows/mypy/badge.svg
	:target: https://github.com/domdfcoding/searchdocs/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.repo-helper.uk/github/domdfcoding/searchdocs/badge.svg
	:target: https://dependency-dash.repo-helper.uk/github/domdfcoding/searchdocs/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/searchdocs/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/searchdocs?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/searchdocs?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/searchdocs
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/searchdocs
	:target: https://pypi.org/project/searchdocs/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/searchdocs?logo=python&logoColor=white
	:target: https://pypi.org/project/searchdocs/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/searchdocs
	:target: https://pypi.org/project/searchdocs/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/searchdocs
	:target: https://pypi.org/project/searchdocs/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/domdfcoding/searchdocs
	:target: https://github.com/domdfcoding/searchdocs/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/searchdocs
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/searchdocs/v0.2.1
	:target: https://github.com/domdfcoding/searchdocs/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/searchdocs
	:target: https://github.com/domdfcoding/searchdocs/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2023
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/searchdocs
	:target: https://pypi.org/project/searchdocs/
	:alt: PyPI - Downloads

.. end shields

Installation
--------------

.. start installation

``searchdocs`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install searchdocs

.. end installation
