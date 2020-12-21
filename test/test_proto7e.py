from nose.tools import *
from tools.esloging import log_init
log_init(".")
from tools.converter import hexstr2bytes
from protocol.smart7e_protocol import Smart7eProtocol,checksum

proto = Smart7eProtocol()

def test_protocol():
    input = "7e73de8700ff700a002802050604"
    bytes_data = hexstr2bytes(input)

    ret = proto.store_and_find_frame(bytes_data)
    print(str(ret))


def test_decode_array_did():
    input = "7E 3B E6 07 00 0B 00 00 00 D5 23 02 41 E0 1F 3B E6 07 00 01 05 42 AE 00 00 01 05 79 0E 00 00 70 96 00 00 00 7F 2B 0A 00 00 E1 6B 10 00 00 AC"
    txt = proto.to_readable_str(input)
    print(txt)

def test_re_array_pattern():
    import re
    txt = "(u8enum,rw,从机信息命令)(u32,d,本机aid)(u8,d,本机status)(u8,d,从机数目)[(u32,d,从机aid)(u8,d,从机status),从机数目,从机信息]"
    #array_infos = re.findall(r"[\[【]([\w.]*)[,，]([\w]*)[,，]([_\w]*)[】\]]", txt)
    array_infos = re.findall(r"\[([\w, ()]*)[,，]([\w)]*)[,，]([_\w]*)\]", "[(name,12,名称) (name,12,名称),xx,yy] [xiaohong] ")
    print(array_infos)


