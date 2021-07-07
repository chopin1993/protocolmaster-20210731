# encoding:utf-8
import engine
config = engine.get_config()
# """
#     设备加入网关PANID，
#     """
# def test_加入网关():
#     engine.send_local_msg("设置PANID", 11176)
#     engine.expect_local_msg("确认")
#     engine.send_did("WRITE", "开关机E013", "01")
#     engine.expect_did("WRITE", "开关机E013", "01")

def test_制冷开阀():
    # 制冷开阀
    engine.send_did("WRITE", "开关机E013", "01")
    engine.expect_did("WRITE", "开关机E013", "01")
    engine.wait(15)
    engine.send_multi_dids("WRITE", "室外机工作状态E060",
                           "4E 9F 06 00 13 E0 01 01 12 E0 01 00 00 E0 02 00 12 00 E0 02 01 45 01 B7 03 03 23 00 01 B7 03 04 37 00 01 B7 03 05 10 01 01 B7 03 06 10 01 01 B7 03 0F 34 02 5C E0 03 01 02 03 51 E0 01 01 09 D1 02 01 00 0A D1 02 01 00 05 D1 02 06 00 05 D1 02 07 00 05 D1 02 08 00 05 D1 02 09 00 05 E0 04 07 35 20 60")
    engine.expect_multi_dids("WRITE", "室外机工作状态E060",
                             "4E 9F 06 00 13 E0 01 01 12 E0 01 00 00 E0 02 00 12 00 E0 02 01 45 01 B7 03 03 23 00 01 B7 03 04 37 00 01 B7 03 05 10 01 01 B7 03 06 10 01 01 B7 03 0F 34 02 5C E0 03 01 02 03 51 E0 01 01 09 D1 02 01 00 0A D1 02 01 00 05 D1 02 06 00 05 D1 02 07 00 05 D1 02 08 00 05 D1 02 09 00 05 E0 04 07 35 20 60")

from autotest.公共用例.public01基本协议测试 import *

测试组说明 = "基本协议类报文测试"
"""
1、常用的基本协议类报文测试，已在公共用例中编写，直接导入即可；
2、针对各产品自身的基础协议，根据需要自定义补充；
"""



def test_应用层通讯协议及版本0002():
    """
    10_应用层通讯协议及版本0002
    """
    #制热，开阀
    # engine.send_did("WRITE", "开关机E013", "01")
    # engine.expect_did("WRITE", "开关机E013", "01")
    # engine.wait(15)
    # engine.send_multi_dids("WRITE", "室外机工作状态E060",
    #                        "4E 9F 06 00 13 E0 01 01 12 E0 01 01 00 E0 02 00 12 00 E0 02 01 45 01 B7 03 03 23 00 01 B7 03 04 37 00 01 B7 03 05 10 01 01 B7 03 06 10 01 01 B7 03 0F 34 02 5C E0 03 01 02 03 51 E0 01 01 09 D1 02 01 00 0A D1 02 01 00 05 D1 02 06 00 05 D1 02 07 00 05 D1 02 08 00 05 D1 02 09 00 05 E0 04 07 35 20 60 85")
    # engine.expect_multi_dids("WRITE", "室外机工作状态E060",
    #                          "4E 9F 06 00 13 E0 01 01 12 E0 01 01 00 E0 02 00 12 00 E0 02 01 45 01 B7 03 03 23 00 01 B7 03 04 37 00 01 B7 03 05 10 01 01 B7 03 06 10 01 01 B7 03 0F 34 02 5C E0 03 01 02 03 51 E0 01 01 09 D1 02 01 00 0A D1 02 01 00 05 D1 02 06 00 05 D1 02 07 00 05 D1 02 08 00 05 D1 02 09 00 05 E0 04 07 35 20 60 85")


    engine.send_did("READ", "应用层通讯协议及版本0002")
    engine.expect_did("READ", "应用层通讯协议及版本0002", config["应用层通讯协议及版本0002"])
    engine.send_multi_dids("READ", "设备类型0001", "",
                           "设备描述信息设备制造商0003", "",
                           "DKEY0005", "",
                           "SN0007", "")
    engine.expect_multi_dids("READ", "设备类型0001", config["设备类型0001"],
                             "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"],
                             "DKEY0005", config["DKEY0005"],
                             "SN0007", config["SN0007"])

