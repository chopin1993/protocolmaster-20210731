from protocol.Test_protocol import TestProtocol
from tools.converter import hexstr2bytes
from nose.tools import assert_equal
from protocol.parser_yacc import parse_protocol_bytes
from protocol import ImageProtocol

# def test_yacc():
#     str_value = "u8:STC=0x4e u8:CMD u8:SEQ u16:DID u32:Length  byte[Length]:Data  u8:CS u8:END=0x5f"
#     parse_protocol_bytes(str_value)


def test_protocol():
    msg = "4E 01 00 01 00 04 01 00 00 04 00 10 00 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 00 00 C8 41 A9 5F "
    receive_data = hexstr2bytes(msg)
    pro = ImageProtocol()
    ret = pro.find_frame_in_buff(receive_data)
    assert_equal(ret, (True, 0, len(receive_data)))

