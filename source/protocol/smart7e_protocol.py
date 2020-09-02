# encoding:utf-8
from enum import Enum
from .protocol import Protocol, protocol_register
from .protocol import find_head
from .codec import BinaryEncoder,BinaryDecoder
from tools.converter import hexstr2bytes, str2hexstr
from .data_fragment import *
import time
from .smart7e_DID import *
import struct

SMART_7e_HEAD = bytes([0x7e])

class DIDLocal(Enum):
    ASK_APPLICATION_ADDR = 0x05
    SET_APPLICATION_ADDR = 0x01
    READ_APPLICATION_ADDR = 0x03

class CMD(Enum):
    READ = 0x02
    WRTIE = 0x7

class LocalFBD(Protocol):
    def __init__(self, cmd, data):
        self.cmd = cmd
        self.data = data

    def encode(self, encoder):
        encoder.encode_u8(self.cmd.value)
        if self.cmd == DIDLocal.SET_APPLICATION_ADDR:
            encoder.encode_u32(self.data)


class RemoteFBD(Protocol):

    @staticmethod
    def create(cmd, did_name, data):
        did_class = find_class_by_name(did_name)
        if did_class is None:
            return None
        did = did_class(data)
        return RemoteFBD(cmd, did)

    def __init__(self, cmd=None, didunit=None, decoder=None):
        self.didunits = []
        if decoder is None:
            self.cmd = cmd
            self.didunits.append(didunit)
        else:
            self.cmd = CMD(value=decoder.decode_u8())
            while decoder.left_bytes() >= 3:
                did = decoder.decode_u16()
                didunit = decoder.decoder_for_object(find_class_by_did(did))
                self.didunits.append(didunit)

    def encode(self, encoder):
        encoder.encode_u8(self.cmd.value)
        for did in self.didunits:
            encoder.encode_object(did)

    def __str__(self):
       text =" "*2 + "fbd:{0}\n".format(self.cmd.name)
       for did in self.didunits:
           text += " "*4 + str(did)
           text += "\n"
       return text


class Smart7EData(Protocol):
    SEQ = 0
    def __init__(self,src=None, dst=None, fbd=None, decoder=None):
        self.data = None
        if decoder is not None:
            self.data = decoder.data
            decoder.decode_byte()
            self.said = decoder.decode_u32()
            self.taid = decoder.decode_u32()
            self.seq = decoder.decode_u8()
            self.len = decoder.decode_u8()
            if self.is_local():
                self.fbd = decoder.decoder_for_object(LocalFBD)
            else:
                self.fbd = decoder.decoder_for_object(RemoteFBD)
        else:
            self.said = src
            self.taid = dst
            self.fbd = fbd
            self.seq = self.SEQ
            self.SEQ +=1

    def is_local(self):
        return self.said ==0 and self.taid == 0

    def encode(self, encoder):
        encoder.encode_bytes(SMART_7e_HEAD)
        encoder.encode_u32(self.said)
        encoder.encode_u32(self.taid)
        encoder.encode_u8(self.seq)
        if isinstance(self.fbd, bytes) or isinstance(self.fbd, bytearray):
            fbd_data = self.fbd
        else:
            fbd_data = encoder.object2data(self.fbd)
        encoder.encode_u8(len(fbd_data))
        encoder.encode_str(fbd_data)
        encoder.encode_u8(checksum(encoder.get_data()))

    def __str__(self):
        if self.data is not None:
            data = self.data
        else:
            data = BinaryEncoder.object2data(self)
        return str2hexstr(data)

    def to_readable_str(self):
        text = "said:{0},taid:{1},seq:{2}, len:{3}\n".format(self.said, self.taid, self.seq, self.len)
        text += str(self.fbd)
        return text


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

    def to_readable_str(self, text):
        data = hexstr2bytes(text)
        found, start, datalen = self.find_frame_in_buff(data)
        if found:
            data = data[start:start+datalen]
            data = BinaryDecoder.data2object(Smart7EData, data)
            return data.to_readable_str()
        else:
            return "no valid frame"
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