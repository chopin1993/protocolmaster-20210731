#encoding:utf-8
from protocol.smart7e_DID import DIDRemote, to_xls_enum_name
from protocol.data_meta_type import *

# 声明自定义单元
SUPPORT_NAMES = ["传感器数据", "步长"]


def encode_value(value, encoder, **kwargs):
    """
    编码函数
    :param value:本单元的数据
    :param encoder:编码器
    :param kwargs:上下文，key为ctx里面具有did所有的数据域
    """
    did_data = kwargs['ctx'] # ctx
    if to_xls_enum_name("传感器类型", did_data[0]) == r"照度":
        encoder.encode_bcd_u16(value)
    else:
        encoder.encode_bcd_u8(value)


def decode_value(decoder, **kwargs):
    """
    解码函数
    :param decoder:解码器
    :param kwargs:上下文，key为ctx里面具有did所有的数据域
    :return:解码之后的值
    """
    did_data = kwargs['ctx']
    if to_xls_enum_name("传感器类型", did_data[0]) == r"照度":
       value = decoder.decode_bcd_u16()
    else:
       value = decoder.decode_bcd_u8()
    return value

