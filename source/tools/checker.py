# encoding:utf-8

import struct

def checksum(*args):
    """
    1的ascii码为49
    >>> data = bytes([0x31,0x32,0x33])
    >>> checksum(data)
    150
    """
    sum_value = 0
    for data in args:
        for byte in data:
            sum_value += byte
            sum_value &= 0xFF  # 强制截断
    return sum_value
