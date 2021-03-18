# encoding:utf-8
from autotest.公共用例.public常用测试模块 import *
from .常用测试模块 import *

测试组说明 = "功能类报文测试"

channel_dict = {1: '01', 2: '02'}  # 设备通道及对应值


def test_出厂默认参数():
    """
    01_默认出厂参数测试
    1、出厂第一次继电器默认为断开00 通断操作C012
    2、断电后默认上电状态为02上电状态为上次断电状态 继电器上电状态C060
    3、继电器过零保护出厂为2路，可分别设置，默认断开延时5.7ms，默认闭合延时5.0ms  继电器过零点动作延迟时间C020
    4、状态同步默认状态03同时上报设备和网关 主动上报使能标志D005
    """
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")
    engine.send_did("READ", "继电器上电状态C060")
    engine.expect_did("READ", "继电器上电状态C060", "02")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", "00 03")
    engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
    engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 39 32")
    engine.send_did("READ", "继电器过零点动作延迟时间C020", "02")
    engine.expect_did("READ", "继电器过零点动作延迟时间C020", "02 39 32")


def test_通断操作C012():
    """
    02_通断操作C012
    1、查询当前通断状态00
    2、打开通道，然后查询当前通断状态，监测器输出监测正常；
    3、关闭通道，然后查询当前通断状态，监测器输出监测正常；
    """
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")

    engine.add_doc_info("通道1控制通断测试")
    relay_output_test(did="通断操作C012", relay_channel=1, output_channel=[0])

    engine.add_doc_info("通道2控制通断测试")
    relay_output_test(did="通断操作C012", relay_channel=2, output_channel=[1])

    engine.add_doc_info("2个通道同时控制通断测试")
    relay_output_test(did="通断操作C012", relay_channel=3, output_channel=[0, 1])


def test_继电器翻转C018():
    """
    03_继电器翻转C018
    bit5~bit0:1/0表示通道操作/不操作；bit0表示第1个通道，回复时按C012报文格式回复
    1、查询当前通断状态00关闭
    2、继电器翻转，然后查询当前通断状态，监测器输出监测正常；
    3、继电器翻转，然后查询当前通断状态，监测器输出监测正常；
    """
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")

    engine.add_doc_info('通道1控制翻转测试')
    relay_output_test(did="继电器翻转C018", relay_channel=1, output_channel=[0])

    engine.add_doc_info('通道2控制翻转测试')
    relay_output_test(did="继电器翻转C018", relay_channel=2, output_channel=[1])

    engine.add_doc_info('2个通道同时控制翻转测试')
    relay_output_test(did="继电器翻转C018", relay_channel=3, output_channel=[0, 1])


def test_错误类报文测试():
    """
    04_错误类报文测试
    1、数据格式错误，返回错误字00 03（C0 12的数据长度为2，而发送命令中的长度为3）
    2、数据域少一个字节，返回错误字00 01数据域长度错误
    3、发送不存在的数据项FB20，返回错误字00 04数据项不存在
    """
    engine.add_doc_info("1、数据格式错误，返回错误字00 03（C0 12的数据长度为1，而发送命令中的长度为3）")
    engine.send_did("WRITE", "通断操作C012", "01 02 03")
    engine.expect_did("WRITE", "通断操作C012", "03 00")

    engine.add_doc_info("2、数据域少一个字节，返回错误字00 01数据域长度错误")
    engine.add_doc_info('本种错误由载波适配层判断并直接回复，所以SWB总线是监控不到的')
    engine.send_raw("07 05 D0 02 03")
    engine.expect_did("WRITE", "主动上报使能标志D005", "01 00")

    engine.add_doc_info("3、发送不存在的数据项，返回错误字00 04数据项不存在")
    engine.send_did("READ", "总有功电能9010", "")
    engine.expect_did("READ", "总有功电能9010", "04 00")

    engine.wait(10, tips='本轮测试结束')
