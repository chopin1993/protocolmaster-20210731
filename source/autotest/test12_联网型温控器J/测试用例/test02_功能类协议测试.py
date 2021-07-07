# encoding:utf-8
from autotest.公共用例.public常用测试模块 import *

from .常用测试模块 import *

测试组说明 = "功能类报文测试"

channel_dict = {1: '01', 2: '02'}  # 设备通道及对应值


def test_出厂默认参数():
    """
    01_默认出厂参数测试
    1、出厂第一次继电器默认为关机00 开关机E013
    2、状态同步默认状态03同时上报设备和网关 主动上报使能标志D005
    """

    engine.send_multi_dids("WRITE", "室外机工作状态E060",
                           "4E 9F 06 00 13 E0 01 01 12 E0 01 00 00 E0 02 00 12 00 E0 02 01 45 01 B7 03 03 23 00 01 B7 03 04 37 00 01 B7 03 05 10 01 01 B7 03 06 10 01 01 B7 03 0F 34 02 5C E0 03 01 02 03 51 E0 01 01 09 D1 02 01 00 0A D1 02 01 00 05 D1 02 06 00 05 D1 02 07 00 05 D1 02 08 00 05 D1 02 09 00 05 E0 04 07 35 20 60")
    engine.expect_multi_dids("WRITE", "室外机工作状态E060",
                             "4E 9F 06 00 13 E0 01 01 12 E0 01 00 00 E0 02 00 12 00 E0 02 01 45 01 B7 03 03 23 00 01 B7 03 04 37 00 01 B7 03 05 10 01 01 B7 03 06 10 01 01 B7 03 0F 34 02 5C E0 03 01 02 03 51 E0 01 01 09 D1 02 01 00 0A D1 02 01 00 05 D1 02 06 00 05 D1 02 07 00 05 D1 02 08 00 05 D1 02 09 00 05 E0 04 07 35 20 60")

    #开机，开机之后等待2分半以后，阀门打开
    engine.send_did("WRITE", "开关机E013","01" )
    engine.expect_did("WRITE", "开关机E013","01")

    #engine.wait(150)
    engine.send_did("READ", "主动上报使能标志D005","03")
    engine.expect_did("READ", "主动上报使能标志D005", "03 03")
    engine.send_did("READ", "运行模式E012", "")
    engine.expect_did("READ", "运行模式E012", "**")  #FF
    engine.send_did("READ", "设置温度1E002", "")
    engine.expect_did("READ", "设置温度1E002", "**")
    engine.send_did("READ", "按键解锁/锁定E01E")
    engine.expect_did("READ", "按键解锁/锁定E01E", "2B 00 00")
    engine.send_did("READ", "阀门类型配置E10A")
    engine.expect_did("READ", "阀门类型配置E10A", "** **")#01 02
    engine.send_did("READ", "NTC参数配置E066")
    engine.expect_did("READ", "NTC参数配置E066", "00 00 01 00 50 39 00 00")
    engine.send_did("READ", "上报告警信息D105", "00 01")
    engine.expect_did("READ", "上报告警信息D105", "00 00")
    engine.send_did("READ", "风机控制E011", "")
    engine.expect_did("READ", "风机控制E011", "**")#00


def test_阀门类型配置E10A():
    """
    02_阀门类型配置E10A
    1、查询当前通断状态00
    2、打开    relay_output_test(did="阀门类型配置E10A", relay_channel=1, output_channel=[1])
    通道，然后查询当前通断状态，监测器输出监测正常；
    3、关闭通道，然后查询当前通断状态，监测器输出监测正常；
    """

    # engine.add_doc_info("阀门类型配置E10A测试")
    # relay_output_test(did="阀门类型配置E10A", relay_channel=1, output_channel=[0])

    #阀门类型：两线制常开阀
    engine.add_doc_info("两线制常开阀")
    engine.send_did("WRITE", "阀门类型配置E10A", "01 01")
    engine.expect_did("WRITE", "阀门类型配置E10A", "01 01")
    engine.send_did("READ", "阀门类型配置E10A")
    engine.expect_did("READ", "阀门类型配置E10A", "01 01")

    # 阀门类型：两线制常闭阀
    engine.add_doc_info("两线制常闭阀")
    engine.send_did("WRITE", "阀门类型配置E10A", "01 02")
    engine.expect_did("WRITE", "阀门类型配置E10A", "01 02")
    engine.send_did("READ", "阀门类型配置E10A")
    engine.expect_did("READ", "阀门类型配置E10A", "01 02")

    # 阀门类型：三线一控常开阀
    engine.add_doc_info("三线一控常开阀")
    engine.send_did("WRITE", "阀门类型配置E10A", "01 03")
    engine.expect_did("WRITE", "阀门类型配置E10A", "01 03")
    engine.send_did("READ", "阀门类型配置E10A", "")
    engine.expect_did("READ", "阀门类型配置E10A", "01 03")

    # 阀门类型：三线一控常闭阀
    engine.add_doc_info("三线一控常闭阀")
    engine.send_did("WRITE", "阀门类型配置E10A", "01 04")
    engine.expect_did("WRITE", "阀门类型配置E10A", "01 04")
    engine.send_did("READ", "阀门类型配置E10A", "")
    engine.expect_did("READ", "阀门类型配置E10A", "01 04")

    # 阀门类型：三线两控阀
    engine.add_doc_info("三线两控阀")
    engine.send_did("WRITE", "阀门类型配置E10A", "01 05")
    engine.expect_did("WRITE", "阀门类型配置E10A", "01 05")
    engine.send_did("READ", "阀门类型配置E10A", "")
    engine.expect_did("READ", "阀门类型配置E10A", "01 05")






def test_开关机E013():
    """
    03_开关机E013
    1、查询当前开关机状态00
    2、打开    relay_output_test(did="开关机E013", relay_channel=1, output_channel=[1])
通道，然后查询当前开关机状态，监测器输出监测正常；
    3、关机，然后查询当前开关机状态，监测器输出监测正常；
    """


    #关机
    engine.send_did("WRITE", "开关机E013", "00")
    engine.expect_did("WRITE", "开关机E013", "00")
    #读取关机状态
    engine.send_did("READ", "开关机E013")
    engine.expect_did("READ", "开关机E013", "00")

    # 开机
    engine.send_did("WRITE", "开关机E013", "01")
    engine.expect_did("WRITE", "开关机E013", "01")
    # 读取开机状态
    engine.send_did("READ", "开关机E013")
    engine.expect_did("READ", "开关机E013", "01")

def test_按键解锁锁定E01E():

    """
    04_按键解锁/锁定E01E
    1、设置锁定，然后查询当前按键状态
    2、设置解锁，然后查询当前按键状态；
    """
    # 锁定
    engine.send_did("WRITE", "按键解锁/锁定E01E", "2B 00 01")
    engine.expect_did("WRITE", "按键解锁/锁定E01E", "2B 00 01")
    # 读取当前按键状态
    engine.send_did("READ", "按键解锁/锁定E01E", "")
    engine.expect_did("READ", "按键解锁/锁定E01E", "2B 00 01")

    # 开锁
    engine.send_did("WRITE", "按键解锁/锁定E01E", "2B 00 00")
    engine.expect_did("WRITE", "按键解锁/锁定E01E", "2B 00 00")
    # 读取当前按键状态
    engine.send_did("READ", "按键解锁/锁定E01E", "")
    engine.expect_did("READ", "按键解锁/锁定E01E", "2B 00 00")

def test_风机控制E011():
    """
    05_风机控制E011
    1、设置为低速00
    2、设置为中速01
    3、设置为高速02
    4、设置为自动03；
    """
    # 设置为低速00
    engine.send_did("WRITE", "风机控制E011", "00")
    engine.expect_did("WRITE", "风机控制E011", "00")
    # 读取当前风速
    engine.send_did("READ", "风机控制E011", "")
    engine.expect_did("READ", "风机控制E011", "00")

    # 设置为中速01
    engine.send_did("WRITE", "风机控制E011", "01")
    engine.expect_did("WRITE", "风机控制E011", "01")
    # 读取当前风速
    engine.send_did("READ", "风机控制E011", "")
    engine.expect_did("READ", "风机控制E011", "01")


    # 设置为高速02
    engine.send_did("WRITE", "风机控制E011", "02")
    engine.expect_did("WRITE", "风机控制E011", "02")
    # 读取当前风速
    engine.send_did("READ", "风机控制E011", "")
    engine.expect_did("READ", "风机控制E011", "02")


    # 设置为自动03
    engine.send_did("WRITE", "风机控制E011", "03")
    engine.expect_did("WRITE", "风机控制E011", "03")
    # 读取当前风速
    engine.send_did("READ", "风机控制E011", "")
    engine.expect_did("READ", "风机控制E011", "03")



    engine.wait(10, tips='本轮测试结束')