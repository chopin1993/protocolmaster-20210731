#encoding:utf-8
from enum import Enum
from tools.converter import bytearray2str,str2hexstr
from protocol.codec import BinaryEncoder,BinaryDecoder
import json
from json import JSONDecodeError
from protocol.DataMetaType import *

class ErrorCode(Enum):
    NO_ERROR = 0
    OTHER_ERROR= 0x0f
    LEN_ERROR = 0x01
    BUFFER_ERR = 0x02
    DATA_ERR = 0x03
    DID_ERROR = 0x04
    DEV_BUSY = 0x05
    NO_RETURN = 0x10

_all_did = dict()

def did_register(media_class):
    global _all_did
    _all_did[media_class.__name__] = media_class
    return media_class

def find_class_by_name(name):
    if name in _all_did.keys():
        return _all_did[name]
    else:
        try:
           did = int(name, base=16)
           return find_class_by_did(did)
        except ValueError as error:
            return None
        return None

def find_class_by_did(did):
    for value in _all_did.values():
        if value.DID == did:
            return value
    return  create_remote_class(str(did), did, [])


def get_all_DID():
    return _all_did

class DIDRemote(object):
    DID=0xff00
    SUPPORTS_DIDS = []
    MEMBERS = []

    @classmethod
    def is_support_did(cls, did):
        if did in cls.SUPPORTS_DIDS:
            return True
        elif did == cls.DID:
            return True
        else:
            return False

    def __init__(self, data=None, decoder=None):
        self.units = []
        self.is_error = False
        self.data = bytes()

        for member in self.MEMBERS:
            meta_data = DataMetaType.create(member)
            if meta_data is not None:
                self.declare_metadata(meta_data)
            else:
                print("error not support meta type", member)

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
                    if decoder.left_bytes() > 0:
                        unit.decode(decoder)
                        txt += str(unit)
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

@did_register
class DIDSoftversion(DIDRemote):
    DID=0x0003
    def __init__(self,data=None, decoder=None):
        super(DIDSoftversion, self).__init__(data,decoder=decoder)
        self.declare_metadata(DataCString("softVersion"))

@did_register
class DIDDebug(DIDRemote):
    DID=0xff00
    def __init__(self, data=None, decoder=None):
        super(DIDDebug, self).__init__(data,decoder=decoder)
        self.declare_metadata(DataU8("choice"))


def create_remote_class(name, did, member):
    cls = type(name, (DIDRemote,), {})
    cls.DID = did
    cls.MEMBERS = member
    did_register(cls)
    return cls


def sync_json_dids():
    ret = 0
    err1 = ""
    with open("smart7E.json", "r") as handle:
        dids = None
        try:
            dids = json.load(handle)
            for did in dids['DIDS']:
                cls = find_class_by_name(did['name'])
                if cls is not None:
                    cls.DID = int(did["did"], base=16)
                    cls.MEMBERS = did['member']
                else:
                    create_remote_class(did['name'], int(did["did"], base=16), did['member'])
        except JSONDecodeError as err:
            ret = -1
            err1 = str(err)
            print(err)
        except Exception as err:
            ret = -1
            err1 = str(err)
        print(dids)
    return ret, err1

sync_json_dids()

