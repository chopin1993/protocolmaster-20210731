# encoding:utf-8
import struct


def hexstr2bytes(string):
    """
    >>> data = " 0x31  0x32  0x33 "
    >>> hexstr2bytes(data)
    '123'
    """
    string = string.strip()
    hex_data = bytes([])
    for byte in string.split(" "):
        if byte is '':
            continue
        for i in range(0, len(byte), 2):
            hex_data += struct.pack("@B", int(byte[i:i+2], 16))
    return hex_data


def str2hexstr(string):
    des = ""
    if isinstance(string, str):
        string = bytes(string, encoding="utf-8")
    for byte in string:
        des += "%02x" %(byte)
        des += " "
    return des.strip().upper()


def u32tohexstr(nb):
    nb = struct.pack("@I", nb)
    hex = str2hexstr(nb)
    return hex


def u16tohexstr(nb):
    nb = struct.pack("@H", nb)
    hex = str2hexstr(nb)
    return hex


def u8tohexstr(value):
    return "{:0>2x}".format(value)

def str2bytearray(string):
    out = bytes(string, encoding="utf-8")
    return out


def bytearray2str(bytes):
    out = ""
    for x in bytes:
        out += chr(x)
    return out


def toint(value):
    pass

