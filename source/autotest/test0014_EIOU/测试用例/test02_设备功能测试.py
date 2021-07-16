# encoding:utf-8
# 导入测试引擎
# from autotest.公共用例.public05远程升级测试 import *
import engine
from .常用测试模块 import *

测试组说明 = "设备功能测试"


def test_出厂默认参数():
    """
    01_默认为禁能模式
    :return:
    """
    engine.send_did('READ', 'IO配置D201')
    engine.expect_did('READ', 'IO配置D201', '01 FF 02 FF 03 FF 04 F 05 FF 06 FF 07 FF 08 FF 09 FF')


def test_local_button():
    """
    02_本地按键测试
    1.按键短按：6s以内，设备复位；
    2.按键长按：6s以上，设备运行指示灯快闪提示并进行恢复出厂设置；
    3.读取复位次数FF A4；触发短按（6s内）；再次读取复位次数，期待值为上次值+1；
    4.配置各路IO使能，读取复位次数；触发长按（6s）；再次获取复位次数；
    :return:
    """
    # 读取设备复位次数
    engine.add_doc_info('测试节点：读取设备复位次数')
    engine.send_did('READ', '设备复位FFA4', '01')
    engine.expect_did('READ', '设备复位FFA4', '01', '** **')        # 两个字节

    # 短按本地按键复位
    engine.add_doc_info('测试节点：短按本地按键复位')
    engine.set_device_sensor_status("按键输入", '短按', channel=0)        # 验证代码

    # 再次读取设备复位次数
    engine.add_doc_info('测试节点：检查两次读取的次数，是否为增1关系')
    engine.send_did('READ', '设备复位FFA4', '01')
    engine.expect_did('READ', '设备复位FFA4', '01', '** **')

    # 回复出厂前设备参数
    engine.add_doc_info('测试节点：设置各IO类型均为使能模式')
    engine.send_did('WRITE', 'IO配置D201', '01 00 02 01 03 02 04 03 05 20 06 21 07 22 08 23 09 24')
    engine.expect_did('WRITE', 'IO配置D201', '01 00 02 01 03 02 04 03 05 20 06 21 07 22 08 23 09 24')
    # 获取复位次数
    engine.add_doc_info('测试节点：获取复位次数')
    engine.send_did('READ', '设备复位FFA4', '01')
    engine.expect_did('READ', '设备复位FFA4', '01', '** **')
    # 长按本地按键回复出厂
    engine.add_doc_info('测试节点：长按本地按键回复出厂')
    engine.set_device_sensor_status("按键输入", '长按', channel=0)    # 验证代码
    # 读取IO模式
    engine.send_did('READ', 'IO配置D201')
    engine.expect_did('READ', 'IO配置D201', '01 FF 02 FF 03 FF 04 F 05 FF 06 FF 07 FF 08 FF 09 FF')
    # 再次获取复位次数
    engine.add_doc_info('测试节点：再次获取复位次数')
    engine.send_did('READ', '设备复位FFA4', '01')
    engine.expect_did('READ', '设备复位FFA4', '01', '** **')
