# encoding:utf-8
from enum import Enum
from .protocol import Protocol
from .protocol import find_head
from .data_fragment import *
import time
from .smart7e_DID import DIDRemote
from .codec import BinaryEncoder, BinaryDecoder
from tools.converter import str2hexstr,hexstr2bytes
from esenum import EsEnum
from .data_fragment import DataFragment

SMART_7e_HEAD = bytes([0x7e])


class DIDLocal(EsEnum):
    ASK_APPLICATION_ADDR = 0x05
    SET_APPLICATION_ADDR = 0x01
    READ_APPLICATION_ADDR = 0x03
    ACTION_OK = 0x00
    ACTION_FAIL = 0xff

class CMD(EsEnum):
    READ = 0x02
    WRITE = 0x7


class LocalFBD(DataFragment):
    def __init__(self, cmd=None, data=None, decoder=None):
        if decoder is None:
            self.cmd = cmd
            self.data = data
        else:
            self.cmd = DIDLocal(value=decoder.decode_u8())
            self.data = decoder.decode_left_bytes()

    def encode(self, encoder):
        encoder.encode_u8(self.cmd.value)
        if self.cmd == DIDLocal.SET_APPLICATION_ADDR:
            encoder.encode_u32(self.data)

    def __str__(self):
        return str(self.cmd.name)



class RemoteFBD(DataFragment):

    @staticmethod
    def create(cmd, did_name, data):
        did_class = DIDRemote.find_class_by_name(did_name)
        if did_class is None:
            return None
        did = did_class(data)
        cmd = CMD.to_enum(cmd)
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
                didunit = decoder.decoder_for_object(DIDRemote.find_class_by_did(did))
                self.didunits.append(didunit)

    def encode(self, encoder):
        encoder.encode_u8(self.cmd.value)
        for did in self.didunits:
            encoder.encode_object(did)

    def __str__(self):
       text = self.cmd.name
       for did in self.didunits:
           text += " " + str(did)
       return text


class Smart7EData(DataFragment):
    SEQ = 0
    def __init__(self, src=None, dst=None, fbd=None, decoder=None):
        self.data = None
        if decoder is not None:
            self.data = decoder.data
            decoder.decode_byte()
            self.said = decoder.decode_u32()
            self.taid = decoder.decode_u32()
            self.seq = decoder.decode_u8()
            self.len = decoder.decode_u8()
            fbd_decoder = BinaryDecoder(decoder.decode_bytes(self.len))
            if self.is_local():
                self.fbd = fbd_decoder.decoder_for_object(LocalFBD)
            else:
                self.fbd = fbd_decoder.decoder_for_object(RemoteFBD)
        else:
            self.said = src
            self.taid = dst
            self.fbd = fbd
            self.seq = Smart7EData.SEQ
            Smart7EData.SEQ +=1
            if Smart7EData.SEQ > 127:
                Smart7EData.SEQ = 0
            self.len = self.get_fbd_len()

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

    def get_fbd_len(self):
        encoder = BinaryEncoder()
        if isinstance(self.fbd, bytes) or isinstance(self.fbd, bytearray):
            fbd_data = self.fbd
        else:
            fbd_data = encoder.object2data(self.fbd)
        return len(fbd_data)

    def __str__(self):
        if self.data is not None:
            data = self.data
        else:
            data = BinaryEncoder.object2data(self)
        return str2hexstr(data)

    def to_readable_str(self):
        text = "said:{0} taid:{1} seq:{2} len:{3} fbd:{4}".format(self.said,
                                                                  self.taid,
                                                                  self.seq,
                                                                  self.len,
                                                                  str(self.fbd))
        return text


class Smart7eProtocol(Protocol):

    def __init__(self):
        super(Smart7eProtocol, self).__init__()
        self.image_data = None
        self.did_unit = None

    def __str__(self):
        return self.name

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