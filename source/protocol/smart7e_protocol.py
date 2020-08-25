# encoding:utf-8
from .protocol import Protocol, protocol_register
from .protocol import find_head
from .codec import BinaryEncoder
from tools.converter import hexstr2bytes, str2hexstr
from .data_fragment import *
import time
import struct
SMART_7e_HEAD = bytes([0x7e])


class Smart7EData(Protocol):
    def __init__(self, decoder=None):
        self.data = decoder.data
        if decoder is not None:
            decoder.decode_byte()
            self.said = decoder.decode_u32()
            self.taid = decoder.decode_u32()
            self.seq = decoder.decode_u8()
            self.len = decoder.decode_u8()
            self.fbd = decoder.decode_bytes(self.len)


    def __str__(self):
        return str2hexstr(self.data)


@protocol_register
class Smart7eProtocol(Protocol):

    def __init__(self):
        super(Smart7eProtocol, self).__init__()
        self.image_data = None
        self.did_unit = None

    @staticmethod
    def create_frame(*args, **kwargs):
        protocol = Smart7eProtocol()
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
        return decoder.decoder_for_object(Smart7EData)

    @staticmethod
    def find_frame_in_buff(data):
        start_pos = 0
        total_len = len(data)
        show_time = False
        start = time.time()
        assert not isinstance(data, str)
        while start_pos < (len(data) - 11):
            start_pos = find_head(data, start_pos, SMART_7e_HEAD)
            if start_pos == -1:
                break
            frame_data = data[start_pos:]

            if len(frame_data) < 11:
                break
            data_len = frame_data[10]
            if data_len + 12 > len(frame_data):
                start_pos += 1
                continue
            if frame_data[11 + data_len] != checksum(frame_data[0:data_len + 11]):
                print("check error")
                show_time = True
            else:
                return True,start_pos,data_len+12
        if(show_time):
            print("time const:" ,time.time()-start,"data length",total_len)
        return False, 0, 0