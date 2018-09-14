# encoding:utf-8

import struct


def checksum(*args):
    """
    1的ascii码为49
    >>> data = '123'
    >>> checksum(data)
    150
    """
    sum_value = 0
    for data in args:
        for byte in data:
            sum_value += struct.unpack("@B", byte)[0]
            sum_value &= 0xFF  # 强制截断
    return sum_value
