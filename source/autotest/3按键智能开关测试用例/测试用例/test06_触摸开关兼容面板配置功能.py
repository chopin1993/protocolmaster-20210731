# encoding:utf-8
# 导入测试引擎

from autotest.公共用例.public常用测试模块 import *
from .常用测试模块 import *

测试组说明 = "触摸开关兼容面板配置功能"

config = engine.get_config()
channel_dict = {1: '01', 2: '02', 3: '04'}  # 设备通道及对应值


def test_查询按键默认配置():
    """
    01_查询按键默认配置
    触摸开关默认配置自身继电器，支持读取。按键触发后控制本地继电器动作，背光灯显示本地继电器状态。
    """
    engine.report_check_enable_all(True)  # 打开上报检测
    # 设置测试设备的PANID
    report_gateway_expect(wait_times=[15], ack=True)

    engine.add_doc_info("1、查询默认配置，为自身的AID")
    for channel, value in channel_dict.items():
        engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道=channel)
        engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",
                          设备通道=channel, 被控设备AID=config["测试设备地址"], 被控设备通道=value)

    engine.report_check_enable_all(False)  # 关闭上报检测


def test_配置单灯模式():
    """
    02_配置单灯模式
    1、将触摸开关的按键配置为单灯模式，控制的执行器为抄控器的AID，测试配置正常；
    2、模拟触发触摸开关的按键，测试触摸开关发送的控制报文正常；
    3、再次模拟触发触摸开关的按键，测试触摸开关发送的控制报文正常；
    """
    engine.add_doc_info("1、将触摸开关的按键配置为单灯模式，控制的执行器为抄控器的AID，测试配置正常；")
    for channel, value in channel_dict.items():
        engine.add_doc_info('测试通道{}配置其他设备AID'.format(channel))

        engine.send_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                        设备通道=channel, 被控设备AID=config["抄控器默认源地址"], 被控设备通道=value)
        engine.expect_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                          设备通道=channel, 被控设备AID=config["抄控器默认源地址"], 被控设备通道=value)
        engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道=channel)
        engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",
                          设备通道=channel, 被控设备AID=config["抄控器默认源地址"], 被控设备通道=value)

        for num in range(2):
            engine.add_doc_info('模拟点击控制按键，进行第 {} 次测试'.format(num + 1))
            engine.set_device_sensor_status("按键输入", "短按", channel=(channel - 1))
            engine.expect_did('WRITE', '继电器翻转C018', value, check_seq=False)
            engine.send_did('WRITE', '通断操作C012', value, reply=True)
            engine.wait(5)


def test_配置情景模式():
    """
    03_配置情景模式
    1、配置单组地址广播报文测试，并进行模拟点击验证测试
    2、配置多组地址广播报文测试，并进行模拟点击验证测试
    3、配置面板类设备，超长广播报文，数据域支持127字节测试，并进行模拟点击验证测试
    """
    engine.add_doc_info('03_配置情景模式')
    for channel, value in channel_dict.items():
        button = str(channel).rjust(2, '0')
        engine.add_doc_info('测试通道{}配置其他设备AID'.format(channel))

        engine.add_doc_info('单组地址广播报文测试')
        engine.send_did("WRITE", "情景模式帧体FC29",
                        '01 ' + button + ' 07 02 32 08 12 C0 01 ' + value)
        engine.expect_did("WRITE", "情景模式帧体FC29",
                          '01 ' + button + ' 07 02 32 08 12 C0 01 ' + value)

        for num in range(2):
            engine.add_doc_info('模拟点击控制按键，进行第 {} 次测试'.format(num + 1))
            engine.set_device_sensor_status("按键输入", "短按", channel=(channel - 1))
            engine.expect_did('WRITE', '通断操作C012', value, gids=[2, 5, 6, 12], gid_type='BIT1', taid=0xFFFFFFFF)

            engine.wait(5)

        engine.add_doc_info('多组地址广播报文测试')
        engine.send_did("WRITE", "情景模式帧体FC29",
                        '01 ' + button + ' 13 41 49 03 0A 01 64 02 32 08 13 E0 01 01 41 4B 12 C0 01 ' + value)
        engine.expect_did("WRITE", "情景模式帧体FC29",
                          '01 ' + button + ' 13 41 49 03 0A 01 64 02 32 08 13 E0 01 01 41 4B 12 C0 01 ' + value)

        for num in range(2):
            engine.add_doc_info('模拟点击控制按键，进行第 {} 次测试'.format(num + 1))
            engine.set_device_sensor_status("按键输入", "短按", channel=(channel - 1))
            engine.broadcast_expect_multi_dids('WRITE',
                                               [73], 'U8', '单轨窗帘目标开度0A03', '64',
                                               [2, 5, 6, 12], 'BIT1', '开关机E013', '01',
                                               [75], 'U8', '通断操作C012', value)
            engine.wait(5)

        engine.add_doc_info('面板类设备，超长广播报文，数据域支持127字节测试')
        engine.send_did("WRITE", "情景模式帧体FC29",
                        '01 ' + button + ' 78 '
                                         '9A 07 00 08 00 09 00 0A 00 0B 00 A1 00 A2 00 A3 00 A4 00 A5 00 A6 00 A7 00 A9 00 12 C0 01 08 '
                                         '9A 07 00 08 00 09 00 0A 00 0B 00 A1 00 A2 00 A3 00 A4 00 A5 00 A6 00 A7 00 A9 00 12 C0 01 04 '
                                         '9A 07 00 08 00 09 00 0A 00 0B 00 A1 00 A2 00 A3 00 A4 00 A5 00 A6 00 A7 00 A9 00 12 C0 01 02 '
                                         '96 07 00 08 00 09 00 0A 00 0B 00 A1 00 A2 00 A3 00 A4 00 A5 00 A6 00 12 C0 01 ' + value)
        engine.expect_did("WRITE", "情景模式帧体FC29",
                          '01 ' + button + ' 78 '
                                           '9A 07 00 08 00 09 00 0A 00 0B 00 A1 00 A2 00 A3 00 A4 00 A5 00 A6 00 A7 00 A9 00 12 C0 01 08 '
                                           '9A 07 00 08 00 09 00 0A 00 0B 00 A1 00 A2 00 A3 00 A4 00 A5 00 A6 00 A7 00 A9 00 12 C0 01 04 '
                                           '9A 07 00 08 00 09 00 0A 00 0B 00 A1 00 A2 00 A3 00 A4 00 A5 00 A6 00 A7 00 A9 00 12 C0 01 02 '
                                           '96 07 00 08 00 09 00 0A 00 0B 00 A1 00 A2 00 A3 00 A4 00 A5 00 A6 00 12 C0 01 ' + value)

        for num in range(2):
            engine.add_doc_info('模拟点击控制按键，进行第 {} 次测试'.format(num + 1))
            engine.set_device_sensor_status("按键输入", "短按", channel=(channel - 1))
            engine.broadcast_expect_multi_dids("WRITE",
                                               [7, 8, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 169], "U16",
                                               "通断操作C012", "08",
                                               [7, 8, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 169], "U16",
                                               "通断操作C012", "04",
                                               [7, 8, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 169], "U16",
                                               "通断操作C012", "02",
                                               [7, 8, 9, 10, 11, 161, 162, 163, 164, 165, 166], "U16",
                                               "通断操作C012", value)
            engine.wait(5)


def test_配置信号上报模式():
    """
    04_配置信号上报模式
    """
    engine.report_check_enable_all(True)

    engine.add_doc_info("04_配置信号上报模式")
    for channel, value in channel_dict.items():
        button = str(channel).rjust(2, '0')
        engine.add_doc_info('测试通道{}配置其他设备AID'.format(channel))
        engine.send_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                        设备通道=channel, 被控设备AID=0, 被控设备通道='01')
        engine.expect_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                          设备通道=channel, 被控设备AID=0, 被控设备通道='01')
        engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道=channel)
        engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",
                          设备通道=channel, 被控设备AID=0, 被控设备通道='01')

        for num in range(2):
            engine.add_doc_info('模拟点击控制按键，进行第 {} 次测试'.format(num + 1))
            engine.set_device_sensor_status("按键输入", "短按", channel=(channel - 1))
            engine.expect_did('REPORT', '门磁系统状态SOS状态插卡取电设备状态燃气检测设备C062', '00 ' + button + ' 00 00')
            engine.send_did('REPORT', '门磁系统状态SOS状态插卡取电设备状态燃气检测设备C062', '00 ' + button + ' 00 00', reply=True)
            engine.wait(5)
    engine.report_check_enable_all(False)


def test_按键恢复默认参数():
    """
    05_按键恢复默认参数
    """
    engine.add_doc_info("测试完成，将触摸开关设置回默认参数")
    engine.send_did("WRITE", "复位等待时间CD00", "00")
    engine.expect_did("WRITE", "复位等待时间CD00", "00")

    for channel, value in channel_dict.items():
        engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道=channel)
        engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",
                          设备通道=channel, 被控设备AID=config["测试设备地址"], 被控设备通道=value)
