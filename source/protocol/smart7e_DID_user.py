#encoding:utf-8
from .smart7e_DID import DIDRemote, get_value_txt
from .DataMetaType import *


def sensor_value_encode(value, encoder, **kwargs):
    ctx = kwargs['ctx']
    if get_value_txt("传感器类型",ctx[0]) == r"照度":
        encoder.encode_bcd_u16(value)
    else:
        encoder.encode_bcd_u8(value)


def sensor_value_decode(decoder, **kwargs):
    ctx = kwargs['ctx']
    if get_value_txt("传感器类型",ctx[0]) == r"照度":
       value = decoder.decode_bcd_u16()
    else:
       value = decoder.decode_bcd_u8()
    return value


def get_user_fun(key):
    if key in ["传感器数据","步长"]:
        return sensor_value_encode, sensor_value_decode,None,None
    raise  NotImplementedError