#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import struct

class fileWithStruct(file):

    def read_unpack(self, format):
        """
        read the minimum amount of data from this file enough to unpack the data specified
        by the format variable. See struct.unpack for the formatting options
        """
        return struct.unpack(format, self.read(struct.calcsize(format)))


def main():
    pass

if __name__ == '__main__':
    sys.exit(main())