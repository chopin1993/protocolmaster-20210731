from tools.converter import *
from protocol.monitor9e_protocol import *
from protocol.codec import *
import nose.tools as helper


def test_monitor_find_data():
    prot = Monitor7eProtocol()
    data = hexstr2bytes("bb bb bb bb bb bb bb bb")
    (status, start,len_) = prot.find_frame_in_buff(data)
    helper.assert_false(status)
    data = hexstr2bytes("99 7e ff 00 02 00 00 7e")
    (status, start,len_) = prot.find_frame_in_buff(data)
    helper.assert_true(status)
    helper.assert_equal(start, 1)
    helper.assert_equal(len_, 7)


def test_encode_decoder():
    prot = Monitor7eProtocol()
    data = hexstr2bytes("7e ff 00 05 00 01 7d 5e 7d 5d 7d 5e 7e")
    decoder = BinaryDecoder(data)
    monitor_data = prot.decode(decoder)
    encode_data = BinaryEncoder.object2data(monitor_data)
    helper.assert_equal(encode_data, data, encode_data.hex() + " " + data.hex())
    print(monitor_data.to_readable_str())
