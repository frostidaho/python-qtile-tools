========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |coveralls|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-qtile-tools/badge/?style=flat
    :target: https://readthedocs.org/projects/python-qtile-tools
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/frostidaho/python-qtile-tools.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/frostidaho/python-qtile-tools

.. |coveralls| image:: https://coveralls.io/repos/frostidaho/python-qtile-tools/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/frostidaho/python-qtile-tools

.. |version| image:: https://img.shields.io/pypi/v/qtile-tools.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/qtile-tools

.. |commits-since| image:: https://img.shields.io/github/commits-since/frostidaho/python-qtile-tools/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/frostidaho/python-qtile-tools/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/qtile-tools.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/qtile-tools

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/qtile-tools.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/qtile-tools

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/qtile-tools.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/qtile-tools


.. end-badges

Some addon tools for qtile

* Free software: BSD license

Installation
============

::

    pip install qtile-tools

Documentation
=============

https://python-qtile-tools.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
