# encoding:utf-8
from .protocol import Protocol
from .protocol import find_head
from tools.checker import checksum
import time
from .codec import BinaryEncoder, BinaryDecoder
from tools.converter import *
from tools.esenum import EsEnum
from .data_fragment import DataFragment
from .DataMetaType import *
from .smart_utils import *
from .smart7e_DID import *

SMART_7e_HEAD = bytes([0x7e])


class UpdateStartInfo(DataFragment):
    def __init__(self, decoder=None, **kwargs):
        """
        filesize filecrc blocksize 设备类型 软件版本
        """
        super(UpdateStartInfo, self).__init__()
        self.declare_unit(DataU32("size"))
        self.declare_unit(DataByteArray("crc",length=2))
        self.declare_unit(DataU8("blocksize"))
        self.declare_unit(DataByteArray("devicetype",length=8))
        self.declare_unit(DataCString("softversion"))
        self.load_args(decoder=decoder, **kwargs)


class UpdateFBD(DataFragment):
    def __init__(self, decoder=None, cmd=None, seq=None, ack=None, data=bytes(),crc=None, **kwargs):
        self.cmd = CMD.to_enum(cmd)
        self.seq = seq
        self.ack = ack
        self.crc = crc
        self.length = len(data)
        self.data = data
        if decoder is not None:
            self.decode(decoder)

    def encode(self, encoder):
        encoder.encode_u8(self.cmd.value)
        encoder.encode_u16(self.seq)
        encoder.encode_u8(self.ack)
        encoder.encode_bytes(self.crc)
        encoder.encode_u8(len(self.data))
        encoder.encode_bytes(self.data)

    def decode(self, decoder):
        self.seq = decoder.decode_u16()
        self.ack = decoder.decode_u8()
        self.crc = decoder.decode_bytes(2)
        self.length = decoder.decode_u8()
        self.data = decoder.decode_bytes(self.length)

    def __str__(self):
        txt = "cmd:{0} seq:{1} ack:{2} crc:{3} length:{4:x}".format(
            self.cmd,
            self.seq,
            self.ack,
            str2hexstr(self.crc),
            self.length)
        if self.seq == 0 and len(self.data)>0:
            decoder = BinaryDecoder(self.data)
            txt += str(decoder.decoder_for_object(UpdateStartInfo))
        return txt


class RemoteFBD(DataFragment):

    @staticmethod
    def create(cmd, did_name, data, gids=None, gid_type=None,**kwargs):
        did = DIDRemote.create_did(did_name, data, gids=gids, gid_type=gid_type,**kwargs)
        return RemoteFBD(cmd, did, **kwargs)

    def __init__(self, cmd=None, didunits=None, decoder=None,**kwargs):
        self.didunits = []
        self.cmd = CMD.to_enum(cmd)
        if decoder is None:
            if isinstance(didunits, list):
                self.didunits.extend(didunits)
            else:
                self.didunits.append(didunits)
        else:
            self.decode(decoder, **kwargs)

    def encode(self, encoder):
        encoder.encode_u8(self.cmd.value)
        for did in self.didunits:
            encoder.encode_object(did)

    def decode(self, decoder, **kwargs):
        self.data = bytes(self.cmd.value) + decoder.data
        frame = kwargs['ctx']
        while decoder.left_bytes() >= 3:
            if frame.is_boardcast():
                gid = decoder.decoder_for_object(GID, **kwargs)
                kwargs['gid'] = gid
            if decoder.left_bytes() >= 3:
                did = decoder.decode_u16()
                didunit = decoder.decoder_for_object(DIDRemote.find_class_by_did(did), **kwargs)
                self.didunits.append(didunit)

    def __str__(self):
       text = "{}[{}]".format(self.cmd.name, u8tohexstr(self.cmd.value))
       for did in self.didunits:
           text += "\n    " + str(did)
       return text


class Smart7EData(DataFragment):
    SEQ = 0
    def __init__(self, src=None, dst=None, fbd=None, decoder=None):
        self.data = None
        if decoder is not None:
            self.decode(decoder)
        else:
            self.said = src
            self.taid = dst
            self.fbd = fbd
            self.seq = Smart7EData.SEQ
            Smart7EData.SEQ +=1
            if Smart7EData.SEQ > 127:
                Smart7EData.SEQ = 0
            self.len = self.get_fbd_len()

    def is_reply(self):
        return self.seq&0x80==0x80

    def is_update(self):
        return self.fbd.cmd in [CMD.UPDATE,CMD.UPDATE_PLC]

    def is_local(self):
        return self.said ==0 and self.taid == 0

    def is_boardcast(self):
        return  self.taid == 0xffffffff

    def decode(self, decoder):
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
            cmd = CMD.to_enum(fbd_decoder.decode_u8())
            if cmd in [CMD.UPDATE,CMD.UPDATE_PLC]:
                self.fbd = fbd_decoder.decoder_for_object(UpdateFBD, cmd=cmd, ctx=self)
            else:
                self.fbd = fbd_decoder.decoder_for_object(RemoteFBD, cmd=cmd, ctx=self)

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
        hex_said = u32tohexstr(self.said)
        hex_taid = u32tohexstr(self.taid)
        hex_seq = u8tohexstr(self.seq)
        hex_len = u8tohexstr(self.len)
        text = "said[{}]:{} taid[{}]:{} seq[{}]:{} len[{}]:{} fbd:{}".format(\
            hex_said,self.said,\
            hex_taid,self.taid,\
            hex_seq,self.seq,\
            hex_len,self.len,\
            str(self.fbd))
        return text

    def ack_message(self):
        msg = Smart7EData(self.taid, self.said, self.fbd)
        msg.seq = self.seq|0x80
        return msg


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

