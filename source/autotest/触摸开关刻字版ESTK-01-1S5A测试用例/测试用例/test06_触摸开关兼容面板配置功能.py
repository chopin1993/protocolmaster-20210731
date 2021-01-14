# encoding:utf-8
# 导入测试引擎

from autotest.公共用例.public常用测试模块 import *

测试组说明 = "触摸开关兼容面板配置功能"

config = engine.get_config()


def test_查询按键默认配置():
    """
    1_查询按键默认配置
    触摸开关默认配置自身继电器，支持读取。按键触发后控制本地继电器动作，背光灯显示本地继电器状态。
    """
    engine.report_check_enable_all(True)
    # 设置测试设备的PANID
    set_gw_info()
    engine.wait(20)
    engine.report_check_enable_all(False)

    engine.add_doc_info("1_默认配置，为自身的AID")
    engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道="01")
    engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",
                      设备通道="01", 被控设备AID=config["测试设备地址"], 被控设备通道='01')


def test_配置单灯模式():
    """
    02_配置单灯模式
    1、将触摸开关的按键配置为单灯模式，控制的执行器为抄控器的AID，测试配置正常；
    2、模拟触发触摸开关的按键，测试触摸开关发送的控制报文正常；
    3、再次模拟触发触摸开关的按键，测试触摸开关发送的控制报文正常；
    """
    engine.add_doc_info('2_配置单灯模式')
    engine.add_doc_info("1、将触摸开关的按键配置为单灯模式，控制的执行器为抄控器的AID，测试配置正常；")
    engine.send_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                    设备通道="01", 被控设备AID=config["抄控器默认源地址"], 被控设备通道='01')
    engine.expect_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                      设备通道="01", 被控设备AID=config["抄控器默认源地址"], 被控设备通道='01')
    engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道="01")
    engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",
                      设备通道="01", 被控设备AID=config["抄控器默认源地址"], 被控设备通道='01')

    engine.add_doc_info('模拟点击控制其他设备闭合和断开，进行相关的测试')
    engine.set_device_sensor_status("按键输入", "短按")
    engine.expect_did('WRITE', '继电器翻转C018', '01', check_seq=False)
    engine.send_did('WRITE', '通断操作C012', '01', reply=True)
    engine.wait(2)
    engine.set_device_sensor_status("按键输入", "短按")
    engine.expect_did('WRITE', '继电器翻转C018', '01', check_seq=False)
    engine.send_did('WRITE', '通断操作C012', '00', reply=True)


def test_配置情景模式():
    """
    03_配置情景模式
    """
    engine.add_doc_info('03_配置情景模式')
    engine.add_doc_info('单组地址广播报文测试')
    engine.send_did("WRITE", "情景模式帧体FC29",
                    '01 01 07 02 32 08 13 E0 01 01')
    engine.expect_did("WRITE", "情景模式帧体FC29",
                      '01 01 07 02 32 08 13 E0 01 01')

    engine.add_doc_info('模拟点击控制按键，进行相关的测试')
    engine.set_device_sensor_status("按键输入", "短按")
    engine.expect_did('WRITE', '开关机E013', '01', gids=[2, 5, 6, 12], gid_type='BIT1', taid=0xFFFFFFFF)

    engine.add_doc_info('多组地址广播报文测试')
    engine.send_did("WRITE", "情景模式帧体FC29",
                    '01 01 13 41 49 03 0A 01 64 02 32 08 13 E0 01 01 41 4B 12 C0 01 81')
    engine.expect_did("WRITE", "情景模式帧体FC29",
                      '01 01 13 41 49 03 0A 01 64 02 32 08 13 E0 01 01 41 4B 12 C0 01 81')

    engine.add_doc_info('模拟点击控制按键，进行相关的测试')
    engine.set_device_sensor_status("按键输入", "短按")
    engine.broadcast_expect_multi_dids('WRITE',
                                       [73], 'U8', '单轨窗帘目标开度0A03', '64',
                                       [2, 5, 6, 12], 'BIT1', '开关机E013', '01',
                                       [75], 'U8', '通断操作C012', '81')
    engine.wait(2)
    engine.set_device_sensor_status("按键输入", "短按")
    engine.broadcast_expect_multi_dids('WRITE',
                                       [73], 'U8', '单轨窗帘目标开度0A03', '64',
                                       [2, 5, 6, 12], 'BIT1', '开关机E013', '01',
                                       [75], 'U8', '通断操作C012', '81')

    engine.add_doc_info('面板类设备，超长广播报文，数据域支持127字节测试')
    engine.send_did("WRITE", "情景模式帧体FC29",
                    '01 01 78 '
                    '9A 07 00 08 00 09 00 0A 00 0B 00 A1 00 A2 00 A3 00 A4 00 A5 00 A6 00 A7 00 A9 00 12 C0 01 08 '
                    '9A 07 00 08 00 09 00 0A 00 0B 00 A1 00 A2 00 A3 00 A4 00 A5 00 A6 00 A7 00 A9 00 12 C0 01 04 '
                    '9A 07 00 08 00 09 00 0A 00 0B 00 A1 00 A2 00 A3 00 A4 00 A5 00 A6 00 A7 00 A9 00 12 C0 01 02 '
                    '96 07 00 08 00 09 00 0A 00 0B 00 A1 00 A2 00 A3 00 A4 00 A5 00 A6 00 12 C0 01 01')
    engine.expect_did("WRITE", "情景模式帧体FC29",
                      '01 01 78 '
                      '9A 07 00 08 00 09 00 0A 00 0B 00 A1 00 A2 00 A3 00 A4 00 A5 00 A6 00 A7 00 A9 00 12 C0 01 08 '
                      '9A 07 00 08 00 09 00 0A 00 0B 00 A1 00 A2 00 A3 00 A4 00 A5 00 A6 00 A7 00 A9 00 12 C0 01 04 '
                      '9A 07 00 08 00 09 00 0A 00 0B 00 A1 00 A2 00 A3 00 A4 00 A5 00 A6 00 A7 00 A9 00 12 C0 01 02 '
                      '96 07 00 08 00 09 00 0A 00 0B 00 A1 00 A2 00 A3 00 A4 00 A5 00 A6 00 12 C0 01 01')

    engine.add_doc_info('模拟点击控制按键，进行相关的测试')
    engine.set_device_sensor_status("按键输入", "短按")
    engine.broadcast_expect_multi_dids("WRITE",
                                       [7, 8, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 169], "U16",
                                       "通断操作C012", "08",
                                       [7, 8, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 169], "U16",
                                       "通断操作C012", "04",
                                       [7, 8, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 169], "U16",
                                       "通断操作C012", "02",
                                       [7, 8, 9, 10, 11, 161, 162, 163, 164, 165, 166], "U16",
                                       "通断操作C012", '01')
    engine.wait(2)
    engine.set_device_sensor_status("按键输入", "短按")
    engine.broadcast_expect_multi_dids("WRITE",
                                       [7, 8, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 169], "U16",
                                       "通断操作C012", "08",
                                       [7, 8, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 169], "U16",
                                       "通断操作C012", "04",
                                       [7, 8, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 169], "U16",
                                       "通断操作C012", "02",
                                       [7, 8, 9, 10, 11, 161, 162, 163, 164, 165, 166], "U16",
                                       "通断操作C012", '01')


def test_配置信号上报模式():
    """
    04_配置信号上报模式
    """
    engine.report_check_enable_all(True)

    engine.add_doc_info("04_配置信号上报模式")
    engine.send_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                    设备通道="01", 被控设备AID=0, 被控设备通道='01')
    engine.expect_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                      设备通道="01", 被控设备AID=0, 被控设备通道='01')
    engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道="01")
    engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",
                      设备通道="01", 被控设备AID=0, 被控设备通道='01')

    engine.add_doc_info('模拟点击控制按键，进行相关的测试')
    engine.set_device_sensor_status("按键输入", "短按")
    engine.expect_did('REPORT', '门磁系统状态SOS状态插卡取电设备状态燃气检测设备C062', '00 01 00 00')
    engine.send_did('REPORT', '门磁系统状态SOS状态插卡取电设备状态燃气检测设备C062', '00 01 00 00', reply=True)
    engine.wait(2)
    engine.set_device_sensor_status("按键输入", "短按")
    engine.expect_did('REPORT', '门磁系统状态SOS状态插卡取电设备状态燃气检测设备C062', '00 01 00 00')
    engine.send_did('REPORT', '门磁系统状态SOS状态插卡取电设备状态燃气检测设备C062', '00 01 00 00', reply=True)

    engine.report_check_enable_all(False)


def test_按键恢复默认参数():
    """
    05_按键恢复默认参数
    """
    engine.add_doc_info("测试完成，将触摸开关设置回默认参数")
    engine.send_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                    设备通道="01", 被控设备AID=config["测试设备地址"], 被控设备通道='01')
    engine.expect_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                      设备通道="01", 被控设备AID=config["测试设备地址"], 被控设备通道='01')
    engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道="01")
    engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",
                      设备通道="01", 被控设备AID=config["测试设备地址"], 被控设备通道='01')
