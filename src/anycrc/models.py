# Taken from Greg Cook's CRC catalogue: https://reveng.sourceforge.io/crc-catalogue/all.htm

from dataclasses import dataclass
from dataclasses import fields


def get_hex(value: int, width: int) -> int:
    assert value >= 0
    assert width > 0
    str_width = width // 4
    if width % 4:
        str_width += 1
    return f'0x{{0:0{str_width}x}}'.format(value)


@dataclass
class model:
    width: int
    poly: int
    init: int
    refin: bool
    refout: bool
    xorout: bool
    check: int

    def __iter__(self):
        for field in fields(self):
            yield getattr(self, field.name)

    def __repr__(self) -> str:
        return f'{self.__name__}({self!s})'

    def __str__(self) -> str:
        return str_model(self)


def str_model(model: model) -> str:
    return (f'width={model.width}, '
            f'poly={get_hex(model.poly, model.width)}, '
            f'init={get_hex(model.init, model.width)}, '
            f'refin={model.refin}, '
            f'refout={model.refout}, '
            f'xorout={get_hex(model.xorout, model.width)}, '
            f'check={get_hex(model.check, model.width)}')


models = {
    'CRC3-GSM': model(width=3, poly=0x3, init=0x0, refin=False, refout=False, xorout=0x7, check=0x4),
    'CRC3-ROHC': model(width=3, poly=0x3, init=0x7, refin=True, refout=True, xorout=0x0, check=0x6),
    'CRC4-G-704': model(width=4, poly=0x3, init=0x0, refin=True, refout=True, xorout=0x0, check=0x7),
    'CRC4-INTERLAKEN': model(width=4, poly=0x3, init=0xf, refin=False, refout=False, xorout=0xf, check=0xb),
    'CRC5-EPC-C1G2':  model(width=5, poly=0x09, init=0x09, refin=False, refout=False, xorout=0x00, check=0x00),
    'CRC5-G-704': model(width=5, poly=0x15, init=0x00, refin=True, refout=True, xorout=0x00, check=0x07),
    'CRC5-USB': model(width=5, poly=0x05, init=0x1f, refin=True, refout=True, xorout=0x1f, check=0x19),
    'CRC6-CDMA2000-A': model(width=6, poly=0x27, init=0x3f, refin=False, refout=False, xorout=0x00, check=0x0d),
    'CRC6-CDMA2000-B': model(width=6, poly=0x07, init=0x3f, refin=False, refout=False, xorout=0x00, check=0x3b),
    'CRC6-DARC': model(width=6, poly=0x19, init=0x00, refin=True, refout=True, xorout=0x00, check=0x26),
    'CRC6-G-704': model(width=6, poly=0x03, init=0x00, refin=True, refout=True, xorout=0x00, check=0x06),
    'CRC6-GSM': model(width=6, poly=0x2f, init=0x00, refin=False, refout=False, xorout=0x3f, check=0x13),
    'CRC7-MMC': model(width=7, poly=0x09, init=0x00, refin=False, refout=False, xorout=0x00, check=0x75),
    'CRC7-ROHC': model(width=7, poly=0x4f, init=0x7f, refin=True, refout=True, xorout=0x00, check=0x53),
    'CRC7-UMTS': model(width=7, poly=0x45, init=0x00, refin=False, refout=False, xorout=0x00, check=0x61),
    'CRC8-AUTOSAR': model(width=8, poly=0x2f, init=0xff, refin=False, refout=False, xorout=0xff, check=0xdf),
    'CRC8-BLUETOOTH': model(width=8, poly=0xa7, init=0x00, refin=True, refout=True, xorout=0x00, check=0x26),
    'CRC8-CDMA2000': model(width=8, poly=0x9b, init=0xff, refin=False, refout=False, xorout=0x00, check=0xda),
    'CRC8-DARC': model(width=8, poly=0x39, init=0x00, refin=True, refout=True, xorout=0x00, check=0x15),
    'CRC8-DVB-S2': model(width=8, poly=0xd5, init=0x00, refin=False, refout=False, xorout=0x00, check=0xbc),
    'CRC8-GSM-A': model(width=8, poly=0x1d, init=0x00, refin=False, refout=False, xorout=0x00, check=0x37),
    'CRC8-GSM-B': model(width=8, poly=0x49, init=0x00, refin=False, refout=False, xorout=0xff, check=0x94),
    'CRC8-HITAG': model(width=8, poly=0x1d, init=0xff, refin=False, refout=False, xorout=0x00, check=0xb4),
    'CRC8-I-432-1': model(width=8, poly=0x07, init=0x00, refin=False, refout=False, xorout=0x55, check=0xa1),
    'CRC8-I-CODE': model(width=8, poly=0x1d, init=0xfd, refin=False, refout=False, xorout=0x00, check=0x7e),
    'CRC8-LTE': model(width=8, poly=0x9b, init=0x00, refin=False, refout=False, xorout=0x00, check=0xea),
    'CRC8-MAXIM-DOW': model(width=8, poly=0x31, init=0x00, refin=True, refout=True, xorout=0x00, check=0xa1),
    'CRC8-MIFARE-MAD': model(width=8, poly=0x1d, init=0xc7, refin=False, refout=False, xorout=0x00, check=0x99),
    'CRC8-NRSC-5': model(width=8, poly=0x31, init=0xff, refin=False, refout=False, xorout=0x00, check=0xf7),
    'CRC8-OPENSAFETY': model(width=8, poly=0x2f, init=0x00, refin=False, refout=False, xorout=0x00, check=0x3e),
    'CRC8-ROHC': model(width=8, poly=0x07, init=0xff, refin=True, refout=True, xorout=0x00, check=0xd0),
    'CRC8-SAE-J1850': model(width=8, poly=0x1d, init=0xff, refin=False, refout=False, xorout=0xff, check=0x4b),
    'CRC8-SMBUS': model(width=8, poly=0x07, init=0x00, refin=False, refout=False, xorout=0x00, check=0xf4),
    'CRC8-TECH-3250': model(width=8, poly=0x1d, init=0xff, refin=True, refout=True, xorout=0x00, check=0x97),
    'CRC8-WCDMA': model(width=8, poly=0x9b, init=0x00, refin=True, refout=True, xorout=0x00, check=0x25),
    'CRC10-ATM': model(width=10, poly=0x233, init=0x000, refin=False, refout=False, xorout=0x000, check=0x199),
    'CRC10-CDMA2000': model(width=10, poly=0x3d9, init=0x3ff, refin=False, refout=False, xorout=0x000, check=0x233),
    'CRC10-GSM': model(width=10, poly=0x175, init=0x000, refin=False, refout=False, xorout=0x3ff, check=0x12a),
    'CRC11-FLEXRAY': model(width=11, poly=0x385, init=0x01a, refin=False, refout=False, xorout=0x000, check=0x5a3),
    'CRC11-UMTS': model(width=11, poly=0x307, init=0x000, refin=False, refout=False, xorout=0x000, check=0x061),
    'CRC12-CDMA2000': model(width=12, poly=0xf13, init=0xfff, refin=False, refout=False, xorout=0x000, check=0xd4d),
    'CRC12-DECT': model(width=12, poly=0x80f, init=0x000, refin=False, refout=False, xorout=0x000, check=0xf5b),
    'CRC12-GSM': model(width=12, poly=0xd31, init=0x000, refin=False, refout=False, xorout=0xfff, check=0xb34),
    'CRC12-UMTS': model(width=12, poly=0x80f, init=0x000, refin=False, refout=True, xorout=0x000, check=0xdaf),
    'CRC13-BBC': model(width=13, poly=0x1cf5, init=0x0000, refin=False, refout=False, xorout=0x0000, check=0x04fa),
    'CRC14-DARC': model(width=14, poly=0x0805, init=0x0000, refin=True, refout=True, xorout=0x0000, check=0x082d),
    'CRC14-GSM': model(width=14, poly=0x202d, init=0x0000, refin=False, refout=False, xorout=0x3fff, check=0x30ae),
    'CRC15-CAN': model(width=15, poly=0x4599, init=0x0000, refin=False, refout=False, xorout=0x0000, check=0x059e),
    'CRC15-MPT1327': model(width=15, poly=0x6815, init=0x0000, refin=False, refout=False, xorout=0x0001, check=0x2566),
    'CRC16-ARC': model(width=16, poly=0x8005, init=0x0000, refin=True, refout=True, xorout=0x0000, check=0xbb3d),
    'CRC16-CDMA2000': model(width=16, poly=0xc867, init=0xffff, refin=False, refout=False, xorout=0x0000, check=0x4c06),
    'CRC16-CMS': model(width=16, poly=0x8005, init=0xffff, refin=False, refout=False, xorout=0x0000, check=0xaee7),
    'CRC16-DDS-110': model(width=16, poly=0x8005, init=0x800d, refin=False, refout=False, xorout=0x0000, check=0x9ecf),
    'CRC16-DECT-R': model(width=16, poly=0x0589, init=0x0000, refin=False, refout=False, xorout=0x0001, check=0x007e),
    'CRC16-DECT-X': model(width=16, poly=0x0589, init=0x0000, refin=False, refout=False, xorout=0x0000, check=0x007f),
    'CRC16-DNP': model(width=16, poly=0x3d65, init=0x0000, refin=True, refout=True, xorout=0xffff, check=0xea82),
    'CRC16-EN-13757': model(width=16, poly=0x3d65, init=0x0000, refin=False, refout=False, xorout=0xffff, check=0xc2b7),
    'CRC16-GENIBUS': model(width=16, poly=0x1021, init=0xffff, refin=False, refout=False, xorout=0xffff, check=0xd64e),
    'CRC16-GSM': model(width=16, poly=0x1021, init=0x0000, refin=False, refout=False, xorout=0xffff, check=0xce3c),
    'CRC16-IBM-3740': model(width=16, poly=0x1021, init=0xffff, refin=False, refout=False, xorout=0x0000, check=0x29b1),
    'CRC16-IBM-SDLC': model(width=16, poly=0x1021, init=0xffff, refin=True, refout=True, xorout=0xffff, check=0x906e),
    'CRC16-ISO-IEC-14443-3-A': model(width=16, poly=0x1021, init=0xc6c6, refin=True, refout=True, xorout=0x0000, check=0xbf05),
    'CRC16-KERMIT': model(width=16, poly=0x1021, init=0x0000, refin=True, refout=True, xorout=0x0000, check=0x2189),
    'CRC16-LJ1200': model(width=16, poly=0x6f63, init=0x0000, refin=False, refout=False, xorout=0x0000, check=0xbdf4),
    'CRC16-M17': model(width=16, poly=0x5935, init=0xffff, refin=False, refout=False, xorout=0x0000, check=0x772b),
    'CRC16-MAXIM-DOW': model(width=16, poly=0x8005, init=0x0000, refin=True, refout=True, xorout=0xffff, check=0x44c2),
    'CRC16-MCRF4XX': model(width=16, poly=0x1021, init=0xffff, refin=True, refout=True, xorout=0x0000, check=0x6f91),
    'CRC16-MODBUS': model(width=16, poly=0x8005, init=0xffff, refin=True, refout=True, xorout=0x0000, check=0x4b37),
    'CRC16-NRSC-5': model(width=16, poly=0x080b, init=0xffff, refin=True, refout=True, xorout=0x0000, check=0xa066),
    'CRC16-OPENSAFETY-A': model(width=16, poly=0x5935, init=0x0000, refin=False, refout=False, xorout=0x0000, check=0x5d38),
    'CRC16-OPENSAFETY-B': model(width=16, poly=0x755b, init=0x0000, refin=False, refout=False, xorout=0x0000, check=0x20fe),
    'CRC16-PROFIBUS': model(width=16, poly=0x1dcf, init=0xffff, refin=False, refout=False, xorout=0xffff, check=0xa819),
    'CRC16-RIELLO': model(width=16, poly=0x1021, init=0xb2aa, refin=True, refout=True, xorout=0x0000, check=0x63d0),
    'CRC16-SPI-FUJITSU': model(width=16, poly=0x1021, init=0x1d0f, refin=False, refout=False, xorout=0x0000, check=0xe5cc),
    'CRC16-T10-DIF': model(width=16, poly=0x8bb7, init=0x0000, refin=False, refout=False, xorout=0x0000, check=0xd0db),
    'CRC16-TELEDISK': model(width=16, poly=0xa097, init=0x0000, refin=False, refout=False, xorout=0x0000, check=0x0fb3),
    'CRC16-TMS37157': model(width=16, poly=0x1021, init=0x89ec, refin=True, refout=True, xorout=0x0000, check=0x26b1),
    'CRC16-UMTS': model(width=16, poly=0x8005, init=0x0000, refin=False, refout=False, xorout=0x0000, check=0xfee8),
    'CRC16-USB': model(width=16, poly=0x8005, init=0xffff, refin=True, refout=True, xorout=0xffff, check=0xb4c8),
    'CRC16-XMODEM': model(width=16, poly=0x1021, init=0x0000, refin=False, refout=False, xorout=0x0000, check=0x31c3),
    'CRC17-CAN-FD': model(width=17, poly=0x1685b, init=0x00000, refin=False, refout=False, xorout=0x00000, check=0x04f03),
    'CRC21-CAN-FD': model(width=21, poly=0x102899, init=0x000000, refin=False, refout=False, xorout=0x000000, check=0x0ed841),
    'CRC24-BLE': model(width=24, poly=0x00065b, init=0x555555, refin=True, refout=True, xorout=0x000000, check=0xc25a56),
    'CRC24-FLEXRAY-A': model(width=24, poly=0x5d6dcb, init=0xfedcba, refin=False, refout=False, xorout=0x000000, check=0x7979bd),
    'CRC24-FLEXRAY-B': model(width=24, poly=0x5d6dcb, init=0xabcdef, refin=False, refout=False, xorout=0x000000, check=0x1f23b8),
    'CRC24-INTERLAKEN': model(width=24, poly=0x328b63, init=0xffffff, refin=False, refout=False, xorout=0xffffff, check=0xb4f3e6),
    'CRC24-LTE-A': model(width=24, poly=0x864cfb, init=0x000000, refin=False, refout=False, xorout=0x000000, check=0xcde703),
    'CRC24-LTE-B': model(width=24, poly=0x800063, init=0x000000, refin=False, refout=False, xorout=0x000000, check=0x23ef52),
    'CRC24-OPENPGP': model(width=24, poly=0x864cfb, init=0xb704ce, refin=False, refout=False, xorout=0x000000, check=0x21cf02),
    'CRC24-OS-9': model(width=24, poly=0x800063, init=0xffffff, refin=False, refout=False, xorout=0xffffff, check=0x200fa5),
    'CRC30-CDMA': model(width=30, poly=0x2030b9c7, init=0x3fffffff, refin=False, refout=False, xorout=0x3fffffff, check=0x04c34abf),
    'CRC31-PHILIPS': model(width=31, poly=0x04c11db7, init=0x7fffffff, refin=False, refout=False, xorout=0x7fffffff, check=0x0ce9e46c),
    'CRC32-AIXM': model(width=32, poly=0x814141ab, init=0x00000000, refin=False, refout=False, xorout=0x00000000, check=0x3010bf7f),
    'CRC32-AUTOSAR': model(width=32, poly=0xf4acfb13, init=0xffffffff, refin=True, refout=True, xorout=0xffffffff, check=0x1697d06a),
    'CRC32-BASE91-D': model(width=32, poly=0xa833982b, init=0xffffffff, refin=True, refout=True, xorout=0xffffffff, check=0x87315576),
    'CRC32-BZIP2': model(width=32, poly=0x04c11db7, init=0xffffffff, refin=False, refout=False, xorout=0xffffffff, check=0xfc891918),
    'CRC32-CD-ROM-EDC': model(width=32, poly=0x8001801b, init=0x00000000, refin=True, refout=True, xorout=0x00000000, check=0x6ec2edc4),
    'CRC32-CKSUM': model(width=32, poly=0x04c11db7, init=0x00000000, refin=False, refout=False, xorout=0xffffffff, check=0x765e7680),
    'CRC32-ISCSI': model(width=32, poly=0x1edc6f41, init=0xffffffff, refin=True, refout=True, xorout=0xffffffff, check=0xe3069283),
    'CRC32-ISO-HDLC': model(width=32, poly=0x04c11db7, init=0xffffffff, refin=True, refout=True, xorout=0xffffffff, check=0xcbf43926),
    'CRC32-JAMCRC': model(width=32, poly=0x04c11db7, init=0xffffffff, refin=True, refout=True, xorout=0x00000000, check=0x340bc6d9),
    'CRC32-MEF': model(width=32, poly=0x741b8cd7, init=0xffffffff, refin=True, refout=True, xorout=0x00000000, check=0xd2c22f51),
    'CRC32-MPEG-2': model(width=32, poly=0x04c11db7, init=0xffffffff, refin=False, refout=False, xorout=0x00000000, check=0x0376e6e7),
    'CRC32-XFER': model(width=32, poly=0x000000af, init=0x00000000, refin=False, refout=False, xorout=0x00000000, check=0xbd0be338),
    'CRC40-GSM': model(width=40, poly=0x0004820009, init=0x0000000000, refin=False, refout=False, xorout=0xffffffffff, check=0xd4164fc646),
    'CRC64-ECMA-182': model(width=64, poly=0x42f0e1eba9ea3693, init=0x0000000000000000, refin=False, refout=False, xorout=0x0000000000000000, check=0x6c40df5f0b497347),
    'CRC64-GO-ISO': model(width=64, poly=0x000000000000001b, init=0xffffffffffffffff, refin=True, refout=True, xorout=0xffffffffffffffff, check=0xb90956c775a41001),
    'CRC64-MS': model(width=64, poly=0x259c84cba6426349, init=0xffffffffffffffff, refin=True, refout=True, xorout=0x0000000000000000, check=0x75d4b74f024eceea),
    'CRC64-REDIS': model(width=64, poly=0xad93d23594c935a9, init=0x0000000000000000, refin=True, refout=True, xorout=0x0000000000000000, check=0xe9c6d914c4b8d9ca),
    'CRC64-WE': model(width=64, poly=0x42f0e1eba9ea3693, init=0xffffffffffffffff, refin=False, refout=False, xorout=0xffffffffffffffff, check=0x62ec59e3f1a4f00a),
    'CRC64-XZ': model(width=64, poly=0x42f0e1eba9ea3693, init=0xffffffffffffffff, refin=True, refout=True, xorout=0xffffffffffffffff, check=0x995dc9bbdf1939fa),
}

aliases = {
    'CRC4-ITU': 'CRC4-G-704',
    'CRC5-EPC': 'CRC5-EPC-C1G2',
    'CRC5-ITU': 'CRC5-G-704',
    'CRC6-ITU': 'CRC6-G-704',
    'CRC7': 'CRC7-MMC',
    'CRC8': 'CRC8-SMBUS',
    'CRC8-AES': 'CRC8-TECH-3250',
    'CRC8-EBU': 'CRC8-TECH-3250',
    'CRC8-ITU': 'CRC8-I-432-1',
    'CRC8-MAXIM': 'CRC8-MAXIM-DOW',
    'DOW-CRC': 'CRC8-MAXIM-DOW',
    'CRC10': 'CRC10-ATM',
    'CRC10-I-610': 'CRC10-ATM',
    'CRC11': 'CRC11-FLEXRAY',
    '3GPP': 'CRC12-UMTS',
    'CRC12': 'CRC12-UMTS',
    'X-CRC12': 'CRC12-DECT',
    'CRC15': 'CRC15-CAN',
    'ARC': 'CRC16-ARC',
    'CRC16': 'CRC16-ARC',
    'CRC16-ACORN': 'CRC16-XMODEM',
    'CRC16-AUG-CCITT': 'CRC16-SPI-FUJITSU',
    'CRC16-AUTOSAR': 'CRC16-IBM-3740',
    'CRC16-BLUETOOTH': 'CRC16-KERMIT',
    'CRC16-BUYPASS': 'CRC16-UMTS',
    'CRC16-CCITT': 'CRC16-KERMIT',
    'CRC16-CCITT-FALSE': 'CRC16-IBM-3740',
    'CRC16-CCITT-TRUE': 'CRC16-KERMIT',
    'CRC16-DARC': 'CRC16-GENIBUS',
    'CRC16-EPC': 'CRC16-GENIBUS',
    'CRC16-EPC-C1G2': 'CRC16-GENIBUS',
    'CRC16-IEC-61158-2': 'CRC16-PROFIBUS',
    'CRC16-ISO-HDLC': 'CRC16-IBM-SDLC',
    'CRC16-ISO-IEC-14443-3-B': 'CRC16-IBM-SDLC',
    'CRC16-I-CODE': 'CRC16-GENIBUS',
    'CRC16-LHA': 'CRC16-ARC',
    'CRC16-LTE': 'CRC16-XMODEM',
    'CRC16-MAXIM': 'CRC16-MAXIM-DOW',
    'CRC16-VERIFONE': 'CRC16-UMTS',
    'CRC16-V-41-LSB': 'CRC16-KERMIT',
    'CRC16-V-41-MSB': 'CRC16-XMODEM',
    'CRC16-X-25': 'CRC16-IBM-SDLC',
    'CRC-A': 'CRC16-ISO-IEC-14443-3-A',
    'CRC-CCITT': 'CRC16-KERMIT',
    'CRC-IBM': 'CRC16-ARC',
    'KERMIT': 'CRC16-KERMIT',
    'MODBUS': 'CRC16-MODBUS',
    'R-CRC16': 'CRC16-DECT-R',
    'X-CRC16': 'CRC16-DECT-X',
    'XMODEM': 'CRC16-XMODEM',
    'ZMODEM': 'CRC16-XMODEM',
    'CRC24': 'CRC24-OPENPGP',
    'B-CRC32': 'CRC32-BZIP2',
    'CRC32': 'CRC32-ISO-HDLC',
    'CRC32C': 'CRC32-ISCSI',
    'CRC32D': 'CRC32-BASE91-D',
    'CRC32Q': 'CRC32-AIXM',
    'CRC32-AAL5': 'CRC32-BZIP2',
    'CRC32-ADCCP': 'CRC32-ISO-HDLC',
    'CRC32-DECT-B': 'CRC32-BZIP2',
    'CRC32-BASE91-C': 'CRC32-ISCSI',
    'CRC32-CASTAGNOLI': 'CRC32-ISCSI',
    'CRC32-INTERLAKEN': 'CRC32-ISCSI',
    'CRC32-POSIX': 'CRC32-CKSUM',
    'CRC32-V-42': 'CRC32-ISO-HDLC',
    'CRC32-XZ': 'CRC32-ISO-HDLC',
    'CKSUM': 'CRC32-CKSUM',
    'JAMCRC': 'CRC32-JAMCRC',
    'PKZIP': 'CRC32-ISO-HDLC',
    'XFER': 'CRC32-XFER',
    'CRC64': 'CRC64-ECMA-182',
    'CRC64-GO-ECMA': 'CRC64-XZ',
}
