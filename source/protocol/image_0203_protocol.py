# encoding:utf-8
from .protocol import Protocol
from .protocol import find_head
from .codec import BinaryEncoder
from tools.converter import hexstr2bytes, str2hexstr
from .data_fragment import *
import time
import struct
from protocol.data_fragment import DataFragment
IMG0203_HEAD = bytes([0x54,0x17,0xfe,0x02])
IMG0203_TAIL = 0x03


class ThremalImageData(DataFragment):
    def __init__(self, width, height, data):
        self.width = width
        self.height = height
        self.data = data

    def get_data(self):
        return self.data

    def __str__(self):
        return "img data"


# 'u8:STC=0x02 u8:CMD  u32:Length  byte[Length]:Data  u8:CS u8:END=0x03'

class ImageProtocol0203(Protocol):

    def __init__(self):
        super(ImageProtocol0203, self).__init__()
        self.image_data = None
        self.did_unit = None

    @staticmethod
    def create_frame(*args, **kwargs):
        protocol = ImageProtocol0203()
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
        decoder.decode_bytes(1) # skip start
        cmd = decoder.decode_bytes(1)
        self.length = decoder.decode_uint()
        self.width = decoder.decode_u16()
        self.height = decoder.decode_u16()
        self.image_data = decoder.decode_bytes (self.width*self.height*2)
        return ThremalImageData(self.width, self.height, self.image_data)

    @staticmethod
    def find_frame_in_buff(data):
        start_pos = 0
        total_len = len(data)
        show_time = False
        start = time.time()
        assert  not isinstance(data, str)
        while start_pos < (len(data) - 11):
            start_pos = find_head(data, start_pos, IMG0203_HEAD)
            if start_pos == -1:
                break
            start_pos += 3 #skip head
            frame_data = data[start_pos:]

            if len(frame_data) < 8:
                break
            data_len = struct.unpack("I", frame_data[2:6])[0]
            if data_len + 8 > len(frame_data):
                start_pos += 1
                continue
            if frame_data[6 + data_len] != checksum(frame_data[1:data_len + 6]):
                print("check error")
                show_time = True
                
            if frame_data[7 + data_len] != IMG0203_TAIL:
                start_pos += 1
                show_time = True
                print("tail error")
            else:
                return True,start_pos,data_len+8
        if(show_time):
            print("time const:" ,time.time()-start,"data length",total_len)
        return False, 0, 0