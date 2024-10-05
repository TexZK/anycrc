# cython: language_level = 3
# cython: embedsignature = True
# cython: binding = True

# Copyright (c) 2024 Hussain Al Marzooq
# Edited by Andrea Zoppi

from typing import Union

from bitarray import bitarray

from .models import *

MAX_WIDTH: int = WORDBITS

ByteData = Union[bytes, bytearray, memoryview]
BitData = Union[bytes, bytearray, memoryview, bitarray]


cdef class CRC:

    cdef int ctor_(
        self,
        word_t width,
        word_t poly,
        word_t init,
        char refin,
        char refout,
        word_t xorout,
    ) except -1:

        if width < 1:
            raise ValueError('width must be at least 1 bit')
        if width > WORDBITS:
            raise ValueError(f'width is larger than {WORDBITS} bits')
        cdef word_t mask = (((<word_t>1 << (width - 1)) - 1) << 1) | 1

        if poly <= 0:
            raise ValueError(f'poly must be positive')
        if poly > mask:
            raise ValueError(f'poly is greater than 0x{<int>mask:x}')

        if init > mask:
            raise ValueError(f'init is greater than 0x{<int>mask:x}')

        if xorout > mask:
            raise ValueError(f'xorout is greater than 0x{mask:x}')

        self.model = get_model(width, poly, init, refin, refout, xorout)

        cdef char error_code = init_model(&self.model)
        if error_code:
            raise MemoryError('out of memory')

        crc_table_bytewise(&self.model)
        crc_table_slice16(&self.model)

        self.register = self.model.init

    def __init__(
        self,
        width: int,
        poly: int,
        init: int = 0,
        refin: bool = False,
        refout: bool = False,
        xorout: int = 0,
    ):
        self.ctor_(width, poly, init, refin, refout, xorout)

    def __dealloc__(self):
        free_model(&self.model)

    def __index__(self) -> int:
        return <int>self.register

    cdef word_t get_(self):
        return self.register

    def get(self) -> int:
        return self.get_()

    cdef int set_(self, word_t crc) except -1:
        cdef width_t width = self.model.width
        cdef word_t mask = (((<word_t>1 << (width - 1)) - 1) << 1) | 1
        if crc > mask:
            raise ValueError(f'crc is greater than 0x{<int>mask:x}')
        self.register = crc

    def set(self, crc: int) -> int:
        return self.set_(crc)

    cdef void reset_(self):
        self.register = self.model.init

    def reset(self) -> None:
        self.reset_()

    cdef word_t calc_(self, const byte_t[:] data):
        cdef size_t length = <size_t>len(data) * 8
        return crc_slice16(&self.model, self.register, &data[0], length)

    def calc(self, data: ByteData) -> int:
        return self.calc_(data)

    cdef word_t calc_bits_(self, object bitdata) except? 0xDEAD:
        cdef size_t length = <size_t>len(bitdata)
        if self.model.ref and length % 8 > 0:
            raise ValueError('bit lengths are not supported with reflected CRCs')

        cdef const byte_t[:] view = bitdata
        return crc_slice16(&self.model, self.register, &view[0], length)

    def calc_bits(self, bitdata: BitData) -> int:
        return self.calc_bits_(bitdata)

    cdef word_t update_(self, const byte_t[:] data):
        self.register = self.calc(data)
        return self.register

    def update(self, data: ByteData) -> int:
        return self.update_(data)

    cdef word_t update_bits_(self, object bitdata) except? 0xDEAD:
        self.register = self.calc_bits(bitdata)
        return self.register

    def update_bits(self, bitdata: BitData) -> int:
        return self.update_bits_(bitdata)

    cdef word_t _calc_b_(self, const byte_t[:] data):
        cdef size_t length = <size_t>len(data) * 8
        return crc_bytewise(&self.model, self.register, &data[0], length)

    def _calc_b(self, data: ByteData) -> int:
        return self._calc_b_(data)


def Model(name: str) -> CRC:
    m = models.get(name)
    if m is not None:
        return CRC(m.width, m.poly, m.init, m.refin, m.refout, m.xorout)

    a = aliases.get(name)
    if a is not None:
        m = models[a]
        return CRC(m.width, m.poly, m.init, m.refin, m.refout, m.xorout)

    raise KeyError(f'unknown CRC model {name}')
