# encoding:utf-8
from .protocol import Protocol, protocol_register
from .protocol import find_head
from .codec import BinaryEncoder
from tools.converter import hexstr2str, str2hexstr
from .data_fragment import *

CJT188_HEAD = bytes(0x68)
CJT188_TAIL = bytes(0x16)
CJT188_TYPE_WATER = bytes(0x10)


class DIDReadMeter(object):

    def __init__(self):
        self.serial = 0

    def encode(self, encoder):
        encoder.encode_byte(0x90)
        encoder.encode_byte(0x1f)
        encoder.encode_byte(self.serial)

    def decode(self, decoder):
        pass


@protocol_register
class TestProtocol(Protocol):

    @staticmethod
    def create_frame(*args, **kwargs):
        protocol = TestProtocol(args[0])
        protocol.did_unit = args[1]
        return protocol

    def __init__(self, address=None):
        super(TestProtocol, self).__init__()
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
            padding = bytes(0x00)*(7-len(self.address))
            self.address = padding + self.address

    def encode(self, encoder):
        encoder.encode_str(self.did_unit)
        
    def decode(self, decoder):
        decoder.decode_str(2)
        self.address = decoder.decode_str(7)[::-1]

    @staticmethod
    def find_frame_in_buff(data):
        """
        >>> receive_str = "00 00 00 00 FE FE FE FE FE FE "
        >>> receive_str+="68 10 01 02 03 04 05 06 07 81 16 90 1F 96 00 55 55 05 2C 00 55 55 05 2C 00 00 00 00 00 00 00 00 00 26 16"
        >>> receive_data = hexstr2str(receive_str)
        >>> protocol =  CJT188Protocol()
        >>> protocol.find_frame_in_buff(receive_data)
        (True, 10, 35)
        >>> receive_data = hexstr2str("68 10 01 02 03 04 05 ")
        >>> protocol.find_frame_in_buff(receive_data)
        (False, 0, 0)
        """
        return True, 0, len(data)

