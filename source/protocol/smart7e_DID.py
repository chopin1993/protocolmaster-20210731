#encoding:utf-8
from enum import Enum
import json
from json import JSONDecodeError
from protocol.DataMetaType import *
from copy import deepcopy
from tools.converter import *
import logging
import os
import re

class ErrorCode(Enum):
    NO_ERROR = 0
    OTHER_ERROR= 0x0f
    LEN_ERROR = 0x01
    BUFFER_ERR = 0x02
    DATA_ERR = 0x03
    DID_ERROR = 0x04
    DEV_BUSY = 0x05
    NO_RETURN = 0x10


class SensorType(Enum):
    PERSON_CAMERA = 0x10
    PERSON_IR = 0x0d
    ILLUMINACE = 0x0b


def cmd_filter(name, cmd):
    from .smart7e_protocol import CMD
    ids = cmd
    if cmd == CMD.READ:
        ids = "r"
    elif cmd == CMD.WRITE:
        ids = "w"
    suffixs = name.split("_")
    if len(suffixs) <= 1:
        return False
    return ids in suffixs[-1]

class DIDRemote(Register):
    DID=0xff00
    MEMBERS = []
    REPLY_MEMBERS = []
    READ_MEMBERS = []
    WRITE_MEMBERS = []
    INIT = False
    _all_did = None

    @classmethod
    def get_members(cls, cmd):
        from .smart7e_protocol import CMD
        if cls.INIT is False:
            cls.INIT = True
            cls.READ_MEMBERS =  [deepcopy(meta) for meta in cls.MEMBERS if cmd_filter(meta.name, CMD.READ)]
            cls.WRITE_MEMBERS = [deepcopy(meta) for meta in cls.MEMBERS if cmd_filter(meta.name, CMD.WRITE)]
            cls.REPLY_MEMBERS = [deepcopy(meta) for meta in cls.MEMBERS if cmd_filter(meta.name, "d")]
        if cmd == CMD.READ.name:
            return cls.READ_MEMBERS
        elif cmd == CMD.WRITE.name:
            return cls.WRITE_MEMBERS
        else:
            return cls.REPLY_MEMBERS


    @classmethod
    def get_did_dict(cls, refresh=False):
        if refresh:
            cls._all_did = None
        if DIDRemote._all_did is None:
            cls._all_did = dict()
            sub_classes = cls.__subclasses__()
            for sub_cls in sub_classes:
                cls._all_did[sub_cls.__name__] = sub_cls
        return cls._all_did

    @classmethod
    def find_class_by_name(cls, name, refresh=False):
        all_did = cls.get_did_dict(refresh)
        if name in all_did.keys():
            return all_did[name]
        else:
            try:
                did = int(name, base=16)
                return cls.find_class_by_did(did)
            except ValueError as error:
                return None
            return None

    @classmethod
    def find_class_by_did(cls, did):
        all_did = cls.get_did_dict()
        for value in all_did.values():
            if value.DID == did:
                return value
        return create_remote_class(str(did), did, [])

    @classmethod
    def create_widgets(cls, cmd):
        ask_widgets = [meta.get_widgets() for meta in cls.get_members(cmd)]
        reply_widgets = [meta.get_widgets() for meta in cls.get_members("reply")]
        return ask_widgets, reply_widgets

    @classmethod
    def encode_widgets(cls, widgets, cmd):
        encoder = BinaryEncoder()
        metas =  cls.get_members(cmd)
        for meta, widget in zip(metas, widgets):
            data = deepcopy(encoder.data)
            meta.encode_widget_value(widget, encoder, ctx=data)
        return encoder.get_data()

    @classmethod
    def sync_reply_value(cls, widgets, decoder):
        metas = cls.get_members("reply")
        data = deepcopy(decoder.data)
        for meta, widget in zip(metas, widgets):
            meta.set_widget_value(widget, decoder, ctx=data)

    @classmethod
    def is_value_string(cls, str1):
        metas = cls.get_members("reply")
        if len(metas) == 1 and  isinstance(metas[0], DataCString):
            return True
        else:
            return False

    def __init__(self, data=None, decoder=None):
        self.units = []
        self.is_error = False
        self.data = bytes()
        for member in self.MEMBERS:
            if isinstance(member, DataMetaType):
                self.declare_metadata(member)
            else:
                print("error not support meta type", member)
                assert False

        if decoder is None:
            self.data = data
        else:
            self.len = decoder.decode_u8()
            if self.len & 0x80:
                self.is_error = True
                self.error_code = decoder.decode_u16()
            else:
                self.data = decoder.decode_bytes(self.len)

    def declare_metadata(self, metadata):
        self.units.append(metadata)

    def encode(self, encoder):
        encoder.encode_u16(self.DID)
        assert self.data is not None
        data_len = len(self.data)
        encoder.encode_u8(data_len)
        if data_len > 0:
            encoder.encode_str(self.data)

    def decode(self, decoder):
        len = decoder.decode_u8()
        if len > 0:
            self.data = decoder.decode_bytes(len)
        else:
            self.data = bytes()

    def __str__(self):
        if not self.is_error:
            txt = "{0}-0x{1:0>4x}".format(self.__class__.__name__,self.DID)
            decoder = BinaryDecoder(self.data)
            data = deepcopy(decoder.data)
            if len(self.units) == 1 and decoder.left_bytes():
                unit = self.units[0]
                unit.decode(decoder)
                txt +=" " + unit.value_str()
            elif len(self.units) > 0:
                for unit in self.units:
                    if decoder.left_bytes() > 0:
                        unit.decode(decoder, ctx=data)
                        txt +=" " + str(unit)
            elif len(self.data) > 0:
                txt += " " + str2hexstr(self.data)
            else:
                txt += " no data"
        else:
            name = ErrorCode(value=self.error_code).name
            txt = "{0}-0x{1:0>4x} error:{2} {3}".format(self.__class__.__name__,
                                                        self.DID,
                                                        self.error_code,
                                                        name)
        return txt


class DIDSoftversion(DIDRemote):
    DID=0x0003
    MEMBERS = [DataCString("softVersion_d")]


class DIDDebug(DIDRemote):
    DID=0xff00
    MEMBERS = [DataU8("choice_d")]


def encode_func(value, encoder, **kwargs):
    ctx = kwargs['ctx']
    if ctx[0] == SensorType.ILLUMINACE.value:
        encoder.encode_bcd_u16(value)
    else:
        encoder.encode_bcd_u8(value)


def decode_func(decoder,  **kwargs):
    ctx = kwargs['ctx']
    if ctx[0] == SensorType.ILLUMINACE.value:
       value = decoder.decode_bcd_u16()
    else:
       value = decoder.decode_bcd_u8()
    return value


class DIDReportStep(DIDRemote):
    DID = 0xd103
    MEMBERS = [DataU8Enum("SensorType_wrd", cls=SensorType),
               ContextBaseValue("stepValue_wd", encoder_func=encode_func, decoder_func=decode_func)]

class DIDSensorValue(DIDRemote):
    DID = 0xb701
    MEMBERS = [DataU8Enum("SensorType_rd", cls=SensorType),
               ContextBaseValue("Value_d", encoder_func=encode_func, decoder_func=decode_func)]

def create_remote_class(name, did, member):
    cls = type(name, (DIDRemote,), {})
    cls.DID = did
    cls.MEMBERS = member
    return cls


def sync_xls_dids():
    import xlrd
    config_file = os.path.join("resource", "数据标识分类表格.xls")
    workbook = xlrd.open_workbook(config_file)
    sheet = workbook.sheets()[0]
    did_infos = []
    for row in range(1, sheet.nrows):
        values = sheet.row_values(row, 0,)
        type, did, member_patterns, name = values[1], values[2], values[5],values[11]
        did_infos.append((type, did, member_patterns, name))

    for did_type, did, member_patterns, did_name in did_infos:
        if did_type != "基础":
            continue
        cls = DIDRemote.find_class_by_name(name, refresh=True)
        if cls is None:
            member_configs = re.findall(r"[(（](\w*)[,，](\w*)[,，](\w*)[)）]", member_patterns)
            members = []
            for meta_type, attr, name in member_configs:
                name = name +"_"+ attr
                paras = {}
                paras[name] = meta_type
                members.append(DataMetaType.create(paras))
            create_remote_class(did_name, int(did, base=16), members)

sync_xls_dids()

def sync_json_dids():
    ret = 0
    err1 = ""
    config_file = "smart7E.json"
    with open(config_file, "r", encoding="utf-8") as handle:
        dids = None
        try:
            dids = json.load(handle)
            for did in dids['DIDS']:
                cls = DIDRemote.find_class_by_name(did['name'], refresh=True)
                if cls is not None:
                    cls.DID = int(did["did"], base=16)
                    cls.MEMBERS = [DataMetaType.create(mem) for mem in did['member']]
                else:
                    members = [DataMetaType.create(mem) for mem in did['member']]
                    create_remote_class(did['name'], int(did["did"], base=16), members)
        except JSONDecodeError as err:
            ret = -1
            err1 = str(err)
            logging.exception(err)
        except Exception as err:
            ret = -1
            err1 = str(err)
            logging.exception(err)
    DIDRemote.get_did_dict(refresh=True)
    return ret, err1