#encoding:utf-8
from enum import Enum
import json
from json import JSONDecodeError
from protocol.DataMetaType import *
from copy import deepcopy
from tools.converter import *

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
    if cmd == CMD.READ.name:
        ids = "r"
    elif cmd == CMD.WRTIE.name:
        ids = "w"
    suffixs = name.split("_")
    if len(suffixs) <= 1:
        return False
    return ids in suffixs[-1]

class DIDRemote(object):
    DID=0xff00
    MEMBERS = []
    _all_did = None

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
        ask_widgets = [meta.create_widgets() for meta in cls.MEMBERS if cmd_filter(meta.name, cmd)]
        reply_widgets = [meta.create_widgets() for meta in cls.MEMBERS if cmd_filter(meta.name, "d")]
        return ask_widgets, reply_widgets

    @classmethod
    def encode_widgets(cls, widgets, cmd):
        encoder = BinaryEncoder()
        metas = [meta for meta in cls.MEMBERS if cmd_filter(meta.name, cmd.name)]
        for meta, widget in zip(metas, widgets):
            data = deepcopy(encoder.data)
            meta.encode_widget_value(widget, encoder, ctx=data)
        return encoder.get_data()

    @classmethod
    def sync_reply_value(cls, widgets, decoder):
        metas = [meta for meta in cls.MEMBERS if cmd_filter(meta.name, "d")]
        data = deepcopy(decoder.data)
        for meta, widget in zip(metas, widgets):
            meta.set_widget_value(widget, decoder, ctx=data)

    @classmethod
    def encode_string(cls, str1):
        metas = [meta for meta in cls.MEMBERS if cmd_filter(meta.name, "d")]
        if len(metas) == 1 and  isinstance(metas[0], DataCString):
            str1 = str2bytearray(str1)
        else:
            str1 = hexstr2bytes(str1)
        return str1

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
            if len(self.units) == 1 and decoder.left_bytes():
                unit = self.units[0]
                unit.decode(decoder)
                txt +=" " + unit.value_str()
            elif len(self.units) > 0:
                for unit in self.units:
                    data = deepcopy(decoder.data)
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
        encoder.encode_u16(value)
    else:
        encoder.encode_u8(value)


def decode_func(decoder,  **kwargs):
    ctx = kwargs['ctx']
    if ctx[0] == SensorType.ILLUMINACE.value:
       value = decoder.decode_u16()
    else:
       value = decoder.decode_u8()
    return str(value)


class DIDReportStep(DIDRemote):
    from protocol.DataMetaType import to_number
    DID = 0xd103
    MEMBERS = [DataU8Enum("SensorType_wrd", cls=SensorType),
               ContextBaseValue("stepValue_wd", encoder_func=encode_func, decoder_func=decode_func)]


def create_remote_class(name, did, member):
    cls = type(name, (DIDRemote,), {})
    cls.DID = did
    cls.MEMBERS = member
    return cls


def sync_json_dids():
    ret = 0
    err1 = ""
    with open("smart7E.json", "r") as handle:
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
            print(err)
        except Exception as err:
            ret = -1
            err1 = str(err)
        print(dids)
    DIDRemote.get_did_dict(refresh=True)
    return ret, err1


sync_json_dids()