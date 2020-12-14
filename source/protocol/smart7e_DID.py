#encoding:utf-8
from protocol.DataMetaType import *
from copy import deepcopy
import logging
import re
from collections import OrderedDict
from .smart_utils import *
from tools.filetool import get_config_file
from tools.converter import *
import importlib
from tools.filetool import get_file_list
import os

def cmd_filter(suffixs, cmd):
    ids = cmd
    if cmd == CMD.READ:
        ids = "r"
    elif cmd == CMD.WRITE:
        ids = "w"
    return ids in suffixs


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
    def create_did(self, name, value=None,gid_type="U16",gids=None, **kwargs):
        gid = None
        if gids is not None:
            gid = GID(gid_type, gids)
        did_class = DIDRemote.find_class_by_name(name)
        if did_class is None:
            raise ValueError("did not exist")
        if isinstance(value, str):
            value = hexstr2bytes(value)
        did = did_class(value, gid=gid, **kwargs)
        return did

    @classmethod
    def get_all_types(cls):
        all_types = set()
        for key,value in cls.get_sub_class_dict().items():
            all_types.add(value.TYPE_NAME)
        return list(all_types)

    @classmethod
    def get_members(cls, cmd):
        if cls.INIT is False:
            cls.INIT = True
            cls.READ_MEMBERS = [deepcopy(meta) for meta in cls.MEMBERS if cmd_filter(meta.attr, CMD.READ)]
            cls.WRITE_MEMBERS = [deepcopy(meta) for meta in cls.MEMBERS if cmd_filter(meta.attr, CMD.WRITE)]
            cls.REPLY_MEMBERS = [deepcopy(meta) for meta in cls.MEMBERS if cmd_filter(meta.attr, "d")]
        if isinstance(cmd, CMD):
            cmd = cmd.name
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
        if isinstance(name, int):
            return cls.find_class_by_did(name)
        all_did = cls.get_did_dict(refresh)
        if name in all_did.keys():
            return all_did[name]
        else:
            try:
                did = int(name, base=16)
                return cls.find_class_by_did(did)
            except ValueError as error:
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
        metas = cls.get_members(cmd)
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
        if len(metas) == 1 and isinstance(metas[0], DataCString):
            return True
        else:
            return False

    @classmethod
    def encode_reply(cls, *args, **kwargs):
        encoder = BinaryEncoder()
        idx = 0
        for member in cls.get_members("reply"):
            if member.name in kwargs:
                member.value = kwargs[member.name]
                member.encode(encoder)
            elif len(args) > idx:
                member.value = args[idx]
                member.encode(encoder)
                idx += 1
        return encoder.get_data()

    def __init__(self, data=None, decoder=None, gid=None, **kwargs):
        self.units = []
        self.is_error = False
        self.data = data
        self.reply = False
        self.gid = gid
        self.report = False
        if 'ctx' in kwargs:
            self.ctx = kwargs["ctx"]
            self.reply = self.ctx.is_reply()
        else:
            self.ctx = None
            self.reply = False
        if 'fbd' in kwargs:
            self.report = kwargs["fbd"].is_report()

        for member in self.MEMBERS:
            if isinstance(member, DataMetaType):
                self.declare_metadata(member)
            else:
                print("error not support meta type", member)
                assert False

        if decoder is None:
            if self.data is None:
                encoder = BinaryEncoder()
                for member in self.MEMBERS:
                    if member.name in kwargs:
                        member.value = kwargs[member.name]
                        member.encode(encoder)
                self.data = encoder.get_data()
        else:
            self.decode(decoder,**kwargs)

    def declare_metadata(self, metadata):
        self.units.append(metadata)

    def encode(self, encoder):
        if self.gid is not None:
            encoder.encode_object(self.gid)
        encoder.encode_u16(self.DID)
        assert self.data is not None
        data_len = len(self.data)
        encoder.encode_u8(data_len)
        if data_len > 0:
            encoder.encode_str(self.data)

    def decode(self, decoder, **kwargs):
        self.len = decoder.decode_u8()
        if self.len & 0x80:
            self.is_error = True
            self.data = decoder.peek_bytes(self.len & 0x80)
            self.error_code = decoder.decode_u16()
        else:
            self.data = decoder.decode_bytes(self.len)

    def decode_units(self):
        from .smart7e_protocol import CMD
        outputs = OrderedDict()
        decoder = BinaryDecoder(self.data)
        data = deepcopy(decoder.data)
        if self.reply or self.report:
            metas = self.get_members("reply")
        else:
            metas = self.get_members(CMD.WRITE)
        if len(metas) == 1 and decoder.left_bytes():
            unit = metas[0]
            unit.decode(decoder)
            outputs[unit.name] = unit
        elif len(metas) > 0:
            for unit in metas:
                if decoder.left_bytes() > 0:
                    unit.decode(decoder, ctx=data)
                    outputs[unit.name] = unit
        return outputs

    def __str__(self):
        txt = ""
        if self.gid is not None:
            txt = " " + str(self.gid)
        txt += "did[{}]:{} data[{}]:".format(u16tohexstr(self.DID),
                                             self.__class__.__name__,
                                             str2hexstr(self.data))
        if not self.is_error:
            units = self.decode_units()
            if len(units) == 1:
                txt += " " + list(units.values())[0].value_str()
            elif len(units) > 1:
                for key,value in units.items():
                    txt += " " + str(value)
            elif len(self.data) > 0:
                txt += " " + str2hexstr(self.data)
            else:
                txt += " no data"
        else:
            name = ErrorCode.value_to_name(self.error_code)
            txt += "error:{}".format(name)
        return txt


def create_remote_class(name, did, member,type_name=""):
    from types import new_class
    cls = new_class(name, (DIDRemote,), {})
    cls.DID = did
    cls.MEMBERS = member
    cls.TYPE_NAME = type_name
    return cls


user_func_dict = None


def get_user_fun(name):
    global user_func_dict
    if user_func_dict is None:
        user_func_dict = {}
        files = get_file_list(os.path.join(os.path.dirname(__file__), "dids"))
        for mod_name in files:
            if mod_name.startswith("__"):
                continue
            mod = importlib.import_module("protocol.dids." + os.path.splitext(mod_name)[0])
            names = getattr(mod,"SUPPORT_NAMES")
            encode_func = getattr(mod, "encode_value")
            decode_func = getattr(mod, "decode_value")
            to_value_func = getattr(mod, "to_value", None)
            value_str_func = getattr(mod, "value_str", None)
            for key in names:
                assert key not in user_func_dict,"{} have exist in vs config".format(key)
                user_func_dict[key] = (encode_func, decode_func, to_value_func, value_str_func)
    assert name in user_func_dict
    return user_func_dict[name]


def _create_did_class(did_type, did, member_patterns, did_name):
    member_configs = re.findall(r"[(（]([\w.]*)[,，]([\w]*)[,，]([_\w]*)[)）]", member_patterns)
    members = []
    for meta_type, attr, name in member_configs:
        paras = {}
        paras[name] = meta_type
        paras['attr'] = attr
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

def _parse_dids(sheet):
    did_infos = []
    for row in range(1, sheet.nrows):
        values = sheet.row_values(row, 0, )
        type, did, member_patterns, name = values[1], values[2], values[5], values[11]
        did_infos.append((type, did, member_patterns, name))
    logging.info("did rows %d, rows %d", sheet.nrows-1, len(did_infos))
    for idx,(did_type, did, member_patterns, did_name) in enumerate(did_infos):
        for i in range(10):
           if DIDRemote.find_class_by_name(did_name, refresh=True) is None:
                _create_did_class(did_type, did, member_patterns, did_name)
                if i >=1:
                    logging.warning("%s create %d time",did_name, i+1)
           else:
               continue
    did_dict = DIDRemote.get_did_dict(True)
    all_load =True
    for idx, (did_type, did, member_patterns, did_name) in enumerate(did_infos):
        if did_name not in did_dict:
            logging.error("%s class fail", did_name)
            all_load = False
    if not all_load:
        exit(-1)

enum_dict={}
def _parse_enums(sheet):
    global enum_dict
    name_values = {}
    name = None
    for row in range(0, sheet.nrows):
        values = sheet.row_values(row, 0)
        if name is None:
            name = values[0]
            name_values = {}
        else:
            if values[0] == "":
                enum_dict[name] = name_values
                name = None
            else:
                name_values[values[0]] = int(values[1], base=16)
    enum_dict[name] = name_values


class DIDLocal(object):
    def __init__(self, cmd, units, name):
        self.cmd = cmd
        self.units = units
        self.name = name


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


def _parse_local_cmd(sheet):
    for row in range(1, sheet.nrows):
        values = sheet.row_values(row, 0)
        value, format, cmd_name = int(str(values[0]), base=16), values[1], values[4]
        member_configs = re.findall(r"[(（](\w*)[,，](\w*)[)）]", format)
        units = []
        for meta_type,  name in member_configs:
            paras = {}
            paras[name] = meta_type
            data_meta = DataMetaType.create(paras)
            units.append(data_meta)
        LocalFBD.append_cmd(value, units, cmd_name)


def sync_xls_dids():
    import xlrd
    global enum_dict
    config_file = get_config_file("数据标识分类表格.xls")
    workbook = xlrd.open_workbook(config_file)
    enum_dict = {}
    _parse_enums(workbook.sheet_by_name("enums"))
    _parse_dids(workbook.sheet_by_name("dids"))
    _parse_local_cmd(workbook.sheet_by_name("localcmd"))
    logging.info("load  %d dids ok!!!!!",len(DIDRemote.get_did_dict()))

def to_xls_enum_name(enum_key, value):
    value_dict = enum_dict[enum_key]
    for key,value1 in value_dict.items():
        if value1 == value:
            return  key

sync_xls_dids()