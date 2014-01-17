#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import struct


LITTLE_ENDIAN_FORMAT = '<'
BIG_ENDIAN_FORMAT = '>'
MAGIC_NUMBER_FORMAT = 'BBBB'
FILE_HEADERS_FORMAT = 'HHIIII'
PACKET_HEADERS_FORMAT = 'IIII'


class fileWithStruct(file):

    def read_unpack(self, format):
        """
        read the minimum amount of data from this file enough to unpack the data specified
        by the format variable. See struct.unpack for the formatting options
        """
        size = struct.calcsize(format)

        data = self.read(size)

        if not data:
            return None

        if len(data) != size:
            raise Exception('could only read {} byte(s) but {} bytes are needed (struct format "{}")'.format(len(data), size, format))

        return struct.unpack(format, data)


def discover_endianness(f):
    big_endian_magic_number = (0xa1, 0xb2, 0xc3, 0xd4)

    magic_number = f.read_unpack(MAGIC_NUMBER_FORMAT)

    if magic_number == big_endian_magic_number:
        return BIG_ENDIAN_FORMAT
    elif magic_number == big_endian_magic_number[::-1]:
        return LITTLE_ENDIAN_FORMAT
    else:
        raise Exception('no magic number found')


def _read_headers(f, endianness, format, fields):
    headers = f.read_unpack(endianness + format)
    return {key: headers[i] for i, key in enumerate(fields)} if headers else None


def read_file_headers(f, endianness):
    fields = ('major_version', 'minor_version', 'zone_offset', 'timestamp_accuracy', 'snapshot_length', 'link_layer_header')
    return _read_headers(f, endianness, FILE_HEADERS_FORMAT, fields)


def read_packet_headers(f, endianness):
    fields = ('ts_seconds', 'ts_microseconds', 'data_length', 'untrucated_data_length')
    return _read_headers(f, endianness, PACKET_HEADERS_FORMAT, fields)


def read_packets(f, endianness):
    while True:
        headers = read_packet_headers(f, endianness)
        if headers:
            data = f.read(headers['data_length'])
            yield headers, data
        else:
            break


def main():
    f = fileWithStruct('/tmp/tcpdump.data', 'r')
    endianness = discover_endianness(f)
    file_headers = read_file_headers(f, endianness)
    for headers, data in read_packets(f, endianness):
        print headers



if __name__ == '__main__':
    sys.exit(main())