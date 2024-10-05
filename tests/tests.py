import pytest as _
from bitarray import bitarray

import anycrc


def test_models():
    #The standard test data b'123456789' isn't good enough when testing slice-by-16 because the data length is < 16
    test_data = b'123456789'
    test_data2 = b'abcdefghijklmnopqrstuvwxyz'

    for name, model in anycrc.models.items():
        print(name)
        print(anycrc.str_model(model))

        crc = anycrc.Model(name)
        crc2 = anycrc.Model(name)

        #check to see if the result from the byte-by-byte algorithm matches the check value
        value = crc._calc_b(test_data)
        check = model.check
        print('byte-by-byte:  {} {}'.format(anycrc.get_hex(value, model.width), anycrc.get_hex(check, model.width)))
        assert value == check

        #check to see if the result from the slice-by-16 algorithm matches the byte-by-byte value
        value = crc.calc(test_data2)
        value2 = crc2._calc_b(test_data2)

        print('slice-by-16:   {} {}'.format(anycrc.get_hex(value, model.width), anycrc.get_hex(value2, model.width)))
        assert value == value2

        #process the data one byte at a time
        for c in test_data:
            value = crc.update(c.to_bytes(1, 'little'))

        print('update:        {} {}'.format(anycrc.get_hex(value, model.width), anycrc.get_hex(check, model.width)))
        assert value == check
        crc.reset()

        #with length in bits
        if not model.refin:
            bit_data = bitarray()
            bit_data.frombytes(test_data2)
            crc.update_bits(bit_data[:150])
            value = crc.update_bits(bit_data[150:])
            value2 = crc2._calc_b(test_data2)

            print('bits:          {} {}'.format(anycrc.get_hex(value, model.width), anycrc.get_hex(value2, model.width)))
            assert value == value2
            crc.reset()

        print()


def test_aliases():
    #check that all of the aliases are valid
    for alias, name in anycrc.aliases.items():
        print(alias, end=' ')
        assert name in anycrc.models
        print('OK')

    print()
