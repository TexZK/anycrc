anycrc
======

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |gh_actions|
        | |codecov|
    * - package
      - | |version| |wheel|
        | |supported-versions|
        | |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/anycrc/badge/?style=flat
    :target: https://readthedocs.org/projects/anycrc
    :alt: Documentation Status

.. |gh_actions| image:: https://github.com/TexZK/anycrc/workflows/CI/badge.svg
    :alt: GitHub Actions Status
    :target: https://github.com/TexZK/anycrc

.. |codecov| image:: https://codecov.io/gh/TexZK/anycrc/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://app.codecov.io/github/TexZK/anycrc

.. |version| image:: https://img.shields.io/pypi/v/anycrc.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/anycrc/

.. |wheel| image:: https://img.shields.io/pypi/wheel/anycrc.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/anycrc/

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/anycrc.svg
    :alt: Supported versions
    :target: https://pypi.org/project/anycrc/

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/anycrc.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/anycrc/

.. end-badges

This is a Cython module with bindings to the `crcany <https://github.com/madler/crcany>`_ library.
It supports calculating CRC hashes of arbitary sizes as well as updating a CRC hash over time.


Installation
------------

.. code-block:: shell

    pip install anycrc


Usage
-----

Use an existing model:

.. code-block:: pycon

    >>> import anycrc
    >>> crc32 = anycrc.Model('CRC32-MPEG-2')
    >>> crc32.calc(b'Hello World!')
    2498069329

Read the data in chunks:

.. code-block:: pycon

    >>> crc32.update(b'Hello ')
    3788805874
    >>> crc32.update(b'World!')
    2498069329

The `update()` method changes the internally stored CRC value, while `calc()` doesn't.
You can use `get()` to retrieve the CRC value stored within the object:

.. code-block:: pycon

    >>> crc32.get()
    2498069329


To specify the starting CRC value:

.. code-block:: pycon

    >>> crc32.set(3788805874)
    >>> crc32.calc(b'World!')
    2498069329

To go back to the initial value, use:

.. code-block:: pycon

    >>> crc32.reset()

Create a CRC with specific parameters:

.. code-block:: pycon

    >>> crc32 = anycrc.CRC(width=32, poly=0x04c11db7, init=0xffffffff, refin=False, refout=False, xorout=0x00000000)
    >>> crc32.calc(b'Hello World!')
    2498069329

For non-reflected CRCs, the length of the data can be specified in bits by calling `calc_bits()` or `update_bits()` and passing a `bitarray <https://github.com/ilanschnell/bitarray>`_ object:

.. code-block:: pycon

    >>> from bitarray import bitarray
    >>> crc32 = anycrc.Model('CRC32-MPEG-2')
    >>> bits = bitarray()
    >>> bits.frombytes(b'Hello World!')
    >>> crc32.update_bits(bits[:50])
    >>> crc32.update_bits(bits[50:])
    2498069329

For a list of pre-built models, check `models.py <src/anycrc/models.py>`_.
To get a list of the models at any time, use the following command:

.. code-block:: shell

    python -m anycrc models

The maximum supported CRC width is 64 bits.


Benchmark
---------

+-------------+------------------+---------------+----------+
| Module      | Time Elapsed (s) | Speed (GiB/s) | Relative |
+=============+==================+===============+==========+
| anycrc      |             0.39 |          2.36 |     1.00 |
+-------------+------------------+---------------+----------+
| zlib        |             0.48 |          1.93 |     1.22 |
+-------------+------------------+---------------+----------+
| fastcrc     |             1.50 |          0.62 |     3.81 |
+-------------+------------------+---------------+----------+
| crcmod-plus |             1.52 |          0.61 |     3.85 |
+-------------+------------------+---------------+----------+

Tested on a 10th generation Intel i7 processor.
