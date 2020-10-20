# encoding:utf-8
from .protocol import Protocol
from .protocol import find_head
from .codec import BinaryEncoder
from tools.converter import hexstr2bytes, str2hexstr
from .data_fragment import *
import struct

CJT188_HEAD = bytes([0x4e])
CJT188_TAIL = 0x5f


class ThremalImageData(object):
    def __init__(self, width, height, data):
        self.width = width
        self.height = height
        self.data = data

    def get_data(self):
        return self.data

    def __str__(self):
        return "img data"


# 'u8:STC=0x4e u8:CMD u8:SEQ u16:DID u32:Length  byte[Length]:Data  u8:CS u8:END=0x5f'
class ImageProtocol(Protocol):

    def __init__(self):
        super(ImageProtocol, self).__init__()
        self.image_data = None
        self.did_unit = None

    @staticmethod
    def create_frame(*args, **kwargs):
        protocol = ImageProtocol()
        protocol.did_unit = args[0]
        return protocol

    def __str__(self):
        if self.did_unit:
            return str2hexstr(self.did_unit)
        if self.image_data is not None:
            return str(self.image_data)
        return "not handle data"

    def encode(self, encoder):
        encoder.encode_bytes(self.did_unit)
        return encoder.encode_char(5)

    def decode(self, decoder):
        decoder.decode_bytes(5) # skip start , cmd , seq
        self.length = decoder.decode_uint()
        self.idx = decoder.decode_uint()
        self.width = decoder.decode_u16()
        self.height = decoder.decode_u16()
        self.image_data = decoder.decode_numpy_float(self.width, self.height)
        return ThremalImageData(self.width, self.height, self.image_data)

    @staticmethod
    def find_frame_in_buff(data):
        start_pos = 0
        found = 0
        assert  not isinstance(data, str)
        while start_pos < (len(data) - 11):
            start_pos = find_head(data, start_pos, CJT188_HEAD)
            if start_pos == -1:
                break
            frame_data = data[start_pos:]

            if len(frame_data) < 11:
                break
            data_len = struct.unpack("I", frame_data[5:9])[0]
            if data_len + 11 > len(frame_data):
                start_pos += 1
                continue
            if frame_data[9 + data_len] != checksum(frame_data[0:data_len + 9]):
                start_pos += 1
                continue
            if frame_data[10 + data_len] != CJT188_TAIL:
                start_pos += 1
                continue
            found = 1
            break

        if found:
            return True, start_pos, data_len + 11
        else:
            return False, 0, 0

