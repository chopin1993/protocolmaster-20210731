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

def calc_crc16(data, crc=0):
    for byte in data:
        crc = ((crc>>8)&255) | (crc<<8)
        crc ^= byte
        crc ^= ((crc&0xff)&255) >>4
        crc ^= (crc << 8) << 4
        crc ^=((crc&0xff)<<4)<<1
    return crc

