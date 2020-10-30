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
    TYPE_NAME=""
    INIT = False
    _all_did = None

    @classmethod
    def get_all_types(cls):
        all_types = set()
        for key,value in  cls.get_sub_class_dict().items():
            all_types.add(value.TYPE_NAME)
        return list(all_types)

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

def create_remote_class(name, did, member,type_name=""):
    cls = type(name, (DIDRemote,), {})
    cls.DID = did
    cls.MEMBERS = member
    cls.TYPE_NAME = type_name
    return cls


def _parse_dids(sheet, enum_dict):
    from .smart7e_DID_user import get_user_fun
    did_infos = []
    for row in range(1, sheet.nrows):
        values = sheet.row_values(row, 0, )
        type, did, member_patterns, name = values[1], values[2], values[5], values[11]
        did_infos.append((type, did, member_patterns, name))

    for did_type, did, member_patterns, did_name in did_infos:
        cls = DIDRemote.find_class_by_name(did_name, refresh=True)
        if cls is None:
            member_configs = re.findall(r"[(（](\w*)[,，](\w*)[,，](\w*)[)）]", member_patterns)
            members = []
            for meta_type, attr, name in member_configs:
                name_used = name + "_" + attr
                paras = {}
                paras[name_used] = meta_type
                data_meta = DataMetaType.create(paras)
                if "enum" in meta_type:
                    assert name in enum_dict, name
                    data_meta.name_dict = enum_dict[name]
                elif "vs" == meta_type:
                    encoder_func, decode_func, to_value_func, value_str_func = get_user_fun(name)
                    data_meta.encode_func = encoder_func
                    data_meta.decoder_func = decode_func
                    data_meta.to_value_func = to_value_func
                    data_meta.value_str_func = value_str_func
                members.append(data_meta)
            create_remote_class(did_name, int(did, base=16), members, did_type)


def _parse_enum(sheet):
    name_values = {}
    for row in range(1, sheet.nrows):
        values = sheet.row_values(row, 0, )
        name_values[values[0]] = int(values[1], base=16)
    return name_values

enum_dict={}

def sync_xls_dids():
    import xlrd
    global enum_dict
    config_file = os.path.join("resource", "数据标识分类表格.xls")
    workbook = xlrd.open_workbook(config_file)
    enum_dict = {}
    for name in workbook.sheet_names():
        if name.startswith("enum"):
            enum_dict[name[4:]] = _parse_enum(workbook.sheet_by_name(name))
    sheet = workbook.sheet_by_name("dids")
    _parse_dids(sheet,enum_dict)

def get_value_txt(enum_key, value):
    value_dict = enum_dict[enum_key]
    for key,value1 in value_dict.items():
        if value1 == value:
            return  key

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