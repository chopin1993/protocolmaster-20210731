# encoding:utf-8
from .protocol import Protocol, protocol_register
from .protocol import find_head
from .codec import BinaryEncoder
from tools.converter import hexstr2bytes, str2hexstr
from .data_fragment import *


@protocol_register
class TestProtocol(Protocol):

    def __init__(self):
        super(TestProtocol, self).__init__()
        self.format = 'u8:STC=0x4e u8:CMD u8:SEQ u16:DID u32:Length  byte[Length]:Data  u8:CS u8:END=0x5f'
        self.tree_fragments = parse_protocol_string(self.format)

    @staticmethod
    def find_frame_in_buff(data):
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
            if ord(frame_data[11 + data_len]) != checksum(frame_data[0:data_len + 11]):
                start_pos += 1
                continue
            if frame_data[12 + data_len] != CJT188_TAIL:
                start_pos += 1
                continue
            found = 1
            break

        if found:
            return True, start_pos, data_len + 13
        else:
            return False, 0, 0

