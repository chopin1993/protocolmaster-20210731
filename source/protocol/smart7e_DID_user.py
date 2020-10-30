#encoding:utf-8
from .smart7e_DID import DIDRemote,SensorType
from .DataMetaType import *

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
    MEMBERS = [DataU8Enum("SensorType_wrd", name_dict=SensorType),
               ContextBaseValue("stepValue_wd", encoder_func=encode_func, decoder_func=decode_func)]


class DIDSensorValue(DIDRemote):
    DID = 0xb701
    MEMBERS = [DataU8Enum("SensorType_rd", name_dict=SensorType),
               ContextBaseValue("Value_d", encoder_func=encode_func, decoder_func=decode_func)]
