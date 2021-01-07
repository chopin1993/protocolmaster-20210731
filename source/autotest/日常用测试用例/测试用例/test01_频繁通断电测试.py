# encoding:utf-8

from autotest.公共用例.public常用测试模块 import *

测试组说明 = "基本协议类报文测试"
"""
1、常用的基本协议类报文测试，已在公共用例中编写，直接导入即可；
2、针对各产品自身的基础协议，根据需要自定义补充；
"""


def test_搭建测试环境():
    '''
    00_搭建测试环境
    :return:
    '''
    set_gw_info(aid=config["前置通断电工装AID"],
                pw=config["前置通断电工装PWD"],
                sid=1)


def power_reset_test(num, device_list):
    """
    :param num: 通断电次数
    :param device_list: 待测设备列表
    """
    for i in range(num):
        msg = "第" + str(i + 1) + "次通断电测试: "
        engine.add_doc_info(msg)
        power_control(time=30)
        for aid in device_list:
            aid = int(aid)
            engine.send_did("READ", "设备描述信息设备制造商0003", "", taid=aid)
            engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"], said=aid)

        engine.wait(30)


def test_01_频繁通断电测试():
    """
    01_频繁通断电测试
    """
    power_reset_test(5, [967353, 178288])
