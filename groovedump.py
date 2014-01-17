#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import struct


LITTLE_ENDIAN_STRUCT_FORMAT = '<'
BIG_ENDIAN_STRUCT_FORMAT = '>'


class fileWithStruct(file):

    def read_unpack(self, format):
        """
        read the minimum amount of data from this file enough to unpack the data specified
        by the format variable. See struct.unpack for the formatting options
        """
        return struct.unpack(format, self.read(struct.calcsize(format)))


def discover_endianness(f):
    big_endian_magic_number = (0xa1, 0xb2, 0xc3, 0xd4)

    magic_number = f.read_unpack('BBBB')

    if magic_number == big_endian_magic_number:
        return BIG_ENDIAN_STRUCT_FORMAT
    elif magic_number == big_endian_magic_number[::-1]:
        return LITTLE_ENDIAN_STRUCT_FORMAT
    else:
        raise Exception('no magic number found')


def main():
    pass

if __name__ == '__main__':
    sys.exit(main())