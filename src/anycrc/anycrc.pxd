# cython: language_level = 3
# cython: embedsignature = True
# cython: binding = True

# Copyright (c) 2024 Hussain Al Marzooq

from libc.stdint cimport uint64_t

ctypedef unsigned short width_t
ctypedef unsigned char byte_t


cdef extern from '../../lib/crcany/model.h':
    ctypedef uint64_t word_t

    cdef const width_t WORDBITS

    ctypedef struct model_t:
        width_t width
        char ref
        char rev
        word_t poly
        word_t init
        word_t xorout
        word_t *table

    cdef model_t get_model(
        width_t width,
        word_t poly,
        word_t init,
        char refin,
        char refout,
        word_t xorout
    )
    cdef char init_model(model_t *model)
    cdef void free_model(model_t *model)


cdef extern from '../../lib/crcany/crc.h':
    cdef void crc_table_bytewise(model_t *model)
    cdef word_t crc_bytewise(
        model_t *model,
        word_t crc,
        const void *dat,
        size_t len
    )

    cdef void crc_table_slice16(model_t *model)
    cdef word_t crc_slice16(
        model_t *model,
        word_t crc,
        const void *dat,
        size_t len
    )


cdef class CRC:
    cdef model_t model
    cdef word_t register

    cdef int ctor_(
        self,
        word_t width,
        word_t poly,
        word_t init,
        char refin,
        char refout,
        word_t xorout,
    ) except -1

    cdef word_t get_(self)

    cdef int set_(self, word_t crc) except -1

    cdef void reset_(self)

    cdef word_t calc_(self, const byte_t[:] data)

    cdef word_t calc_bits_(self, object bitdata) except? 0xDEAD

    cdef word_t update_(self, const byte_t[:] data)

    cdef word_t update_bits_(self, object bitdata) except? 0xDEAD

    # byte-by-byte (for testing)
    cdef word_t _calc_b_(self, const byte_t[:] data)
