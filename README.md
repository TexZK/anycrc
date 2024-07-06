This is a Cython module with bindings to the [crcany](https://github.com/madler/crcany) library. It supports calculating CRC hashes of arbitary sizes as well as updating a CRC hash over time. Anycrc supports all of the CRCs listed in the [RevEng CRC Catalogue](https://reveng.sourceforge.io/crc-catalogue/all.htm).

## Installation

`pip install anycrc`

## Usage

Use an existing model:

```python
>>> import anycrc
>>> crc32 = anycrc.Model('CRC32')
>>> crc32.calc(b'Hello World!')
472456355
```

Read the data in chunks:

```python
>>> crc32.update(b'Hello ')
3928882368
>>> crc32.update(b'World!')
472456355
```

The `update` method changes the internally stored CRC value, while `calc` doesn't. You can use `get` to retrieve the CRC value stored within the object:

```python
>>> crc32.get()
472456355
```

To specify the starting CRC value:

```python
>>> crc32.set(3928882368)
>>> crc32.calc('World!')
472456355
```

To go back to the initial value, use:

```python
>>> crc32.reset()
```

Create a CRC with specific parameters:

```python
>>> crc32 = anycrc.CRC(width=32, poly=0x04c11db7, init=0xffffffff, refin=True, refout=True, xorout=0xffffffff)
>>> crc32.calc('Hello World!')
472456355
```

For a list of pre-built models, check [models.py](https://github.com/marzooqy/anycrc/blob/main/src/anycrc/models.py). To get a list of the models at any time, use the following command:

`python -m anycrc models`

The maximum possible CRC width is 128 bits. CRCs with a width larger than 64 bits use the slower byte-by-byte algorithm.

## Benchmark

| Module | Time Elapsed (s) | Speed (GiB/s) | Relative |
|---|:-:|:-:|:-:|
| anycrc | 0.36 | 2.56 | 1.00 |
| zlib | 0.48 | 1.95 | 1.31 |
| fastcrc | 1.50 | 0.62 | 4.13 |
| crcmod-plus | 1.50 | 0.62 | 4.13 |

Tested on a 10th generation Intel i7 processor.
