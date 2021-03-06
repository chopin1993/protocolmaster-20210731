# encoding:utf-8
from tools.checker import checksum
from .protocol import Protocol, protocol_register
from .protocol import find_head
from .codec import BinaryEncoder
from tools.converter import hexstr2bytes, str2hexstr
from .data_container import *

CJT188_HEAD = bytes(0x68)
CJT188_TAIL = bytes(0x16)
CJT188_TYPE_WATER = bytes(0x10)


class DIDReadMeter(object):

    def __init__(self):
        self.serial = 0

    def encode(self, encoder):
        encoder.encode_u8(0x90)
        encoder.encode_u8(0x1f)
        encoder.encode_u8(self.serial)

    def decode(self, decoder):
        pass


@protocol_register
class CJT188Protocol(Protocol):
    """
    >>> encoder = BinaryEncoder()
    >>> protocol = CJT188Protocol()
    >>> encoder.encode_object(protocol)
    >>> str2hexstr(encoder.get_data())
    '68 10 AA AA AA AA AA AA AA 01 03 90 1F 90 61 16'
    """
    @staticmethod
    def create_frame(*args, **kwargs):
        protocol = CJT188Protocol(args[0])
        protocol.did_unit = args[1]
        return protocol

    def __init__(self, address=None):
        super(CJT188Protocol, self).__init__()
        if address is None:
            address = bytes(0xaa)*7
        self.address = address
        self.meter_type = 0x10
        self.cmd = 0x01
        self.length = 0x04
        self.did_unit = DIDReadMeter()
        self.serial = 0x90
        self.name = "CJT188"

    def padding_address(self):
        if len(self.address) != 7:
            padding = chr(0x00)*(7-len(self.address))
            self.address = padding + self.address

    def encode(self, encoder):
        self.padding_address()
        encoder.encode_str(CJT188_HEAD)
        encoder.encode_u8(self.meter_type)
        encoder.encode_str(self.address[::-1])
        encoder.encode_u8(self.cmd)
        length = len(encoder.object2data(self.did_unit))
        encoder.encode_u8(length)
        self.did_unit.serial = self.serial
        encoder.encode_object(self.did_unit)
        encoder.encode_u8(checksum(encoder.get_data()))
        encoder.encode_str(CJT188_TAIL)

    def decode(self, decoder):
        decoder.decode_bytes(2)
        self.address = decoder.decode_bytes(7)[::-1]

    @staticmethod
    def find_frame_in_buff(data):
        """
        >>> receive_str = "00 00 00 00 FE FE FE FE FE FE "
        >>> receive_str+="68 10 01 02 03 04 05 06 07 81 16 90 1F 96 00 55 55 05 2C 00 55 55 05 2C 00 00 00 00 00 00 00 00 00 26 16"
        >>> receive_data = hexstr2bytes(receive_str)
        >>> protocol =  CJT188Protocol()
        >>> protocol.find_frame_in_buff(receive_data)
        (True, 10, 35)
        >>> receive_data = hexstr2bytes("68 10 01 02 03 04 05 ")
        >>> protocol.find_frame_in_buff(receive_data)
        (False, 0, 0)
        """
        start_pos = 0
        found = 0
        while start_pos < (len(data) - 11):
            start_pos = find_head(data, start_pos, CJT188_HEAD)
            if start_pos == -1:
                break
            frame_data = data[start_pos:]
            if len(frame_data) < 11:
                break

            data_len = ord(frame_data[10])

            if data_len + 13 > len(frame_data):
                start_pos += 1
                continue
            if ord(frame_data[11+data_len])  != checksum(frame_data[0:data_len+11]):
                start_pos += 1
                continue
            if frame_data[12+data_len] != CJT188_TAIL:
                start_pos += 1
                continue
            found = 1
            break

        if found:
            return True, start_pos, data_len+13
        else:
            return False, 0, 0

