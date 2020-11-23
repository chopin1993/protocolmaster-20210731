# encoding:utf-8
from .protocol import Protocol
from .protocol import find_head
from tools.checker import checksum
import time
from .codec import BinaryEncoder, BinaryDecoder
from tools.converter import str2hexstr,hexstr2bytes
from tools.esenum import EsEnum
from .data_fragment import DataFragment
from .DataMetaType import *

SMART_7e_HEAD = bytes([0x7e])


class DIDLocal(object):
    def __init__(self, cmd, units, name):
        self.cmd = cmd
        self.units = units
        self.name = name


class CMD(EsEnum):
    NOTIFY = 0x0 #不可靠上报
    REPORT = 0x01 #可靠上报
    READ = 0x02
    SEARCH = 0x03
    FILE = 0x04
    UPDATE = 0x05 #升级
    UPDATE_BIG = 0x06 #大文件升级
    WRITE = 0x7


class LocalFBD(DataFragment):
    CMDS = []

    @staticmethod
    def append_cmd(cmd ,units, txt):
        LocalFBD.CMDS.append(DIDLocal(cmd, units, txt))

    @staticmethod
    def find_cmd(data):
        for cmd in LocalFBD.CMDS:
            if isinstance(data, str):
                if cmd.name == data:
                    return cmd
            elif isinstance(data,int):
                if cmd.cmd == data:
                    return cmd
            else:
                raise ValueError
        print("no proper cmd",data)
        raise NotImplementedError

    def __init__(self, cmd=None, data=None, decoder=None, **kwargs):
        if decoder is None:
            self.cmd = self.find_cmd(cmd).cmd
            self.data = data
            self.kwargs = kwargs
        else:
            self.decode(decoder)

    def encode(self, encoder):
        encoder.encode_u8(self.cmd)
        if len(self.kwargs) == 0:
            if isinstance(self.data, str):
                value = hexstr2bytes(self.data)
                encoder.encode_str(value)
            elif self.data is not None:
                local_cmd = self.find_cmd(self.cmd)
                if len(local_cmd.units) == 1:
                    unit = local_cmd.units[0]
                    unit.value = self.data
                    unit.encode(encoder)
        else:
            local_cmd = self.find_cmd(self.cmd)
            for unit in local_cmd.units:
                if unit.name in self.kwargs:
                    unit.value = self.kwargs[unit.name]
                    unit.encode(encoder)

    def decode(self, decoder):
        self.cmd = decoder.decode_u8()
        self.data = decoder.decode_left_bytes()

    def __str__(self):
        cmd_info = self.find_cmd(self.cmd)
        if len(cmd_info.units) == 0  or self.data is None :
            return cmd_info.name
        else:
            return cmd_info.name + " " + str(self.data)


class GID(DataFragment):
    TYPE_U8 = 1
    TYPE_U16 = 2
    def __init__(self, type=None, gids=None,decoder=None,**kwargs):
        if decoder is None:
            self.type = type
            if isinstance(gids, int):
                gids = [gids]
            self.gids = gids
        else:
            self.decode(decoder)

    def encode(self, encoder):
        data_encoder = BinaryEncoder()
        if isinstance(self.gids, list):
            if self.type == self.TYPE_U8:
                [data_encoder.encode_u8(addr) for addr in self.gids]
            else:
                [data_encoder.encode_u16(addr) for addr in self.gids]
        else:
            data_encoder.encode_str(self.gids)
        address = data_encoder.get_data()
        encoder.encode_u8(self.type<<6|len(address))
        encoder.encode_str(address)

    def decode(self, decoder):
        data = decoder.decode_u8()
        self.type = ((data&0x3f)>>6)
        len = data&0x3f
        if self.type == self.TYPE_U8:
            self.gids = [decoder.decode_u8()  for i in range(0,len)]
        else:
            self.gids = [decoder.decode_u16() for i in range(0, len, 2)]

    def __str__(self):
        str1 = "gid: type-"
        str1 += "u8" if self.type == self.TYPE_U8 else "u16 "
        str1 += str(self.gids)
        str1 += " "
        return str1


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
    def create(cmd, did_name, data, **kwargs):
        did = DIDRemote.create_did(did_name, data, **kwargs)
        return RemoteFBD(cmd, did)

    def __init__(self, cmd=None, didunits=None, decoder=None, gid=None, **kwargs):
        self.didunits = []
        self.cmd = CMD.to_enum(cmd)
        if decoder is None:
            if isinstance(didunits, list):
                self.didunits.extend(didunits)
            else:
                self.didunits.append(didunits)
            self.gid = gid
        else:
            self.data = bytes(self.cmd.value)+decoder.data
            self.gid = None
            ctx = kwargs['ctx']
            if ctx.is_boardcast():
                self.gid = decoder.decoder_for_object(GID,**kwargs)
            else:
                self.gid = None
            while decoder.left_bytes() >= 3:
                did = decoder.decode_u16()
                didunits = decoder.decoder_for_object(DIDRemote.find_class_by_did(did), **kwargs)
                self.didunits.append(didunits)

    def encode(self, encoder):
        encoder.encode_u8(self.cmd.value)
        if self.gid is not None:
            encoder.encode_object(self.gid)
        for did in self.didunits:
            encoder.encode_object(did)

    def __str__(self):
       text = self.cmd.name
       if self.gid is not None:
           text += " " + str(self.gid)
       for did in self.didunits:
           text += " " + str(did)
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
        return self.fbd.cmd == CMD.UPDATE

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
            if cmd == CMD.UPDATE:
                self.fbd = fbd_decoder.decoder_for_object(UpdateFBD, cmd=cmd, ctx=self)
            else:
                self.fbd = fbd_decoder.decoder_for_object(RemoteFBD, cmd=cmd, ctx=self)

    def encode(self, encoder):
        encoder.encode_bytes(SMART_7e_HEAD)
        encoder.encode_u32(self.said)
        encoder.encode_u32(self.taid)
        encoder.encode_u8(self.seq)

        if self.is_boardcast():  #广播需要带有组地址
            if isinstance(self.fbd, RemoteFBD):
                if self.fbd.gid is None:
                    gid = GID(GID.TYPE_U8,0)
                    self.fbd.gid = gid
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

from .smart7e_DID import DIDRemote