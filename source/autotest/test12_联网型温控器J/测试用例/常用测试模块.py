# encoding:utf-8
# 导入测试引擎
import engine
from autotest.公共用例.public常用测试模块 import *
import time

config = engine.get_config()


def read_write_test():
    """
    抄读开关机测试，用时为passed_time
    """
    start_time = time.time()
    engine.wait(1, tips='控制开关机测试')
    engine.send_did("WRITE", "开关机E013", "00")
    engine.expect_did("WRITE", "开关机E013", "00")
    engine.send_did("READ", "开关机E013")
    engine.expect_did("READ", "开关机E013", "00")
    passed_time = time.time() - start_time
    engine.add_doc_info('控制开关机测试，用时为{:.3f}秒'.format(passed_time))
    return passed_time




def report_gateway_expect(expect_value="00", wait_times=[126], ack=True, quit_net=False, wait_enable=True):
    """
    添加上报测试
    :param wait_times:等待时间列表,自定义
    :param expect_value:期望上报的参数
    :param ack:默认为True,应答上报信息；为False时不应答上报信息
    :param quit_net:退网参数，默认为False，不发送退网指令，为True时，发送退网指令
    """

    set_gw_info()  # 设置网关PANID信息，模拟设备入网
    # 定义添加上报
    for i, wait_time in enumerate(wait_times):
        if i != (len(wait_times) - 1):
            ack_action = False
        else:
            ack_action = ack
        engine.wait((wait_time - 1), allowed_message=False)
        engine.expect_multi_dids("REPORT",
                                 "读传感器数据B701", "03 ** **",
                                 "读传感器数据B701", "04 ** **",
                                 "读传感器数据B701", "0F ** **",
                                 "上报告警信息D105", "00 **",
                                 "上报告警信息D105", "02 **",
                                 "阀门开关地暖阀或风机阀E051", "**",
                                 "开关机E013", "**",
                                 "运行模式E012", "**",
                                 "风机控制E011", "**",
                                 "按键解锁/锁定E01E", "** ** **",
                                 "设置温度1E002", "**",
                                 "导致状态改变的控制设备AIDC01A",config["测试设备地址"],ack=ack_action,timeout=2)
    if wait_enable:
        engine.wait(125, allowed_message=False)
    if quit_net:
        engine.send_did("WRITE", "退网通知060B", 退网设备=config["测试设备地址"])


def report_power_on_expect(expect_value="00", wait_times=[115], ack=True, wait_enable=True):
    """
    上电上报测试
    :param expect_value: 期望上报的参数
    :param wait_times: 等待时间列表
    :param ack: 默认为True,应答上报信息；为False时不应答上报信息
    """

    passed_time = power_control()
    engine.send_did("WRITE", "开关机E013", "01")
    engine.expect_did("WRITE", "开关机E013", "01")
    engine.send_multi_dids("WRITE", "室外机工作状态E060",
                           "4E 9F 06 00 13 E0 01 01 12 E0 01 00 00 E0 02 00 12 00 E0 02 01 45 01 B7 03 03 23 00 01 B7 03 04 37 00 01 B7 03 05 10 01 01 B7 03 06 10 01 01 B7 03 0F 34 02 5C E0 03 01 02 03 51 E0 01 01 09 D1 02 01 00 0A D1 02 01 00 05 D1 02 06 00 05 D1 02 07 00 05 D1 02 08 00 05 D1 02 09 00 05 E0 04 07 35 20 60")
    engine.expect_multi_dids("WRITE", "室外机工作状态E060",
                             "4E 9F 06 00 13 E0 01 01 12 E0 01 00 00 E0 02 00 12 00 E0 02 01 45 01 B7 03 03 23 00 01 B7 03 04 37 00 01 B7 03 05 10 01 01 B7 03 06 10 01 01 B7 03 0F 34 02 5C E0 03 01 02 03 51 E0 01 01 09 D1 02 01 00 0A D1 02 01 00 05 D1 02 06 00 05 D1 02 07 00 05 D1 02 08 00 05 D1 02 09 00 05 E0 04 07 35 20 60")

    # engine.expect_multi_dids("READ", "室外机工作状态E060",
    #                          "FF FF FF FF 13 E0 01 01 12 E0 01 00 00 E0 02 00 12 00 E0 02 01 50 01 B7 03 ** ** 00 01 B7 03 04 ** ** 01 B7 03 05 ** ** 01 B7 03 06 ** ** 01 B7 03 0F ** ** 5C E0 03 81 02 83 51 E0 01 01 09 D1 02 01 01 0A D1 02 01 00 05 D1 02 06 01 05 D1 02 07 00 05 D1 02 08 01 05 D1 02 09 00 05 E0 04 07 35 20 60",
    #                          timeout=11,ack=True)

    if passed_time < wait_times[0]:
        engine.add_doc_info('123')
        wait_times[0] = wait_times[0] - passed_time
        engine.expect_multi_dids("WRITE", "室外机工作状态E060",
                                 "FF FF FF FF 13 E0 01 01 12 E0 01 00 00 E0 02 00 12 00 E0 02 01 50 01 B7 03 ** ** 00 01 B7 03 04 ** ** 01 B7 03 05 ** ** 01 B7 03 06 ** ** 01 B7 03 0F ** ** 5C E0 03 81 02 83 51 E0 01 01 09 D1 02 01 01 0A D1 02 01 00 05 D1 02 06 01 05 D1 02 07 00 05 D1 02 08 01 05 D1 02 09 00 05 E0 04 07 35 20 60",
                                 timeout=11, ack=True)

    else:
        engine.add_fail_test('等待时间参数设置错误')
        engine.expect_multi_dids("READ", "室外机工作状态E060",
                             "FF FF FF FF 13 E0 01 01 12 E0 01 00 00 E0 02 00 12 00 E0 02 01 50 01 B7 03 03 22 00 01 B7 03 04 41 00 01 B7 03 05 10 01 01 B7 03 06 20 02 01 B7 03 0F 21 02 5C E0 03 81 02 83 51 E0 01 01 09 D1 02 01 01 0A D1 02 01 00 05 D1 02 06 01 05 D1 02 07 00 05 D1 02 08 01 05 D1 02 09 00 05 E0 04 07 35 20 60",
                             timeout=11, ack=True)

    for i, data in enumerate(wait_times):

        if i != (len(wait_times) - 1):
            ack_action = False
        else:
            ack_action = ack
        engine.expect_multi_dids("READ", "室外机工作状态E060",
                                 "FF FF FF FF 13 E0 01 01 12 E0 01 00 00 E0 02 00 12 00 E0 02 01 50 01 B7 03 03 22 00 01 B7 03 04 41 00 01 B7 03 05 10 01 01 B7 03 06 20 02 01 B7 03 0F 21 02 5C E0 03 81 02 83 51 E0 01 01 09 D1 02 01 01 0A D1 02 01 00 05 D1 02 06 01 05 D1 02 07 00 05 D1 02 08 01 05 D1 02 09 00 05 E0 04 07 35 20 60",
                                 timeout=11, ack=True)

        engine.wait((wait_times[i] - 1), allowed_message=False)

        engine.expect_multi_dids("REPORT",
                                 "读传感器数据B701", "03 ** **",
                                 "读传感器数据B701", "04 ** **",
                                 "读传感器数据B701", "0F ** **",
                                 "上报告警信息D105", "00 **",
                                 "上报告警信息D105", "** **",
                                 "阀门开关地暖阀或风机阀E051", "**",
                                 "开关机E013", "**",
                                 "运行模式E012", "**",
                                 "风机控制E011", "**",
                                 "按键解锁/锁定E01E", "** ** **",
                                 "设置温度1E002", "**",
                                 "导致状态改变的控制设备AIDC01A", config["测试设备地址"], ack=ack_action,timeout=1)
    if wait_enable:
        engine.wait(115, allowed_message=False)
    # engine.expect_multi_dids("READ", "室外机工作状态E060",
    #                          "FF FF FF FF 13 E0 01 01 12 E0 01 00 00 E0 02 00 12 00 E0 02 01 50 01 B7 03 03 22 00 01 B7 03 04 41 00 01 B7 03 05 10 01 01 B7 03 06 20 02 01 B7 03 0F 21 02 5C E0 03 81 02 83 51 E0 01 01 09 D1 02 01 01 0A D1 02 01 00 05 D1 02 06 01 05 D1 02 07 00 05 D1 02 08 01 05 D1 02 09 00 05 E0 04 07 35 20 60",
    #                          timeout=11, ack=True)


def report_expect_test(expect_value="00", wait_times=True, num=True, i=True, passed_time=True, ack=True,
                       wait_enable=True):
    """
        定频上报测试
        :param expect_value: 期望上报的参数
        :param wait_times: 等待时间列表
        :param num: 定频上报次数
        :param i: 默认为0参数
        :param passed_time: 定频上报时间
        :param ack: 默认为True,应答上报信息；为False时不应答上报信息
        """
    if passed_time < wait_times[0]:
        wait_times[0] = wait_times[0] - passed_time
    else:
        engine.add_fail_test('等待时间参数设置错误')

    for i, data in enumerate(wait_times):
        if i != (len(wait_times) - 1):
            ack_action = False
        else:
            ack_action = ack

        engine.wait((wait_times[i] - 1), allowed_message=False)
        engine.expect_multi_dids("REPORT",
                                 "读传感器数据B701", "03 ** **",
                                 "读传感器数据B701", "04 ** **",
                                 "读传感器数据B701", "0F ** **",
                                 config["测试设备地址"], ack=ack_action)
    if wait_enable:
        engine.wait(119, allowed_message=False)



# def relay_output_test(did="开关机E013", relay_channel=1, output_channel=[0]):
#     """
#     :param did: 控制继电器开关的数据标识
#     :param relay_channel: 控制的设备开关机状态
#     :param output_channel: 输出检测接口
#     :return:
#     """
#     send_value = str(relay_channel | 80)
#     if did == "开机E013":
#         send_value = str(relay_channel | 00).rjust(2, '0')
#     expect_value = str(relay_channel | 00).rjust(2, '0')
#     engine.send_did("WRITE", did, send_value)
#     engine.expect_did("WRITE", "开关机E013", expect_value)
#     engine.wait(1)
#     engine.send_did("READ", "开关机E013", "")
#     engine.expect_did("READ", "开关机E013", expect_value)
#     engine.wait(1)
#     engine.add_doc_info('监测器检测被测设备的输出端')
#     # for channel in output_channel:
#     #     engine.expect_cross_zero_status(channel, 1)
#
#     send_value = str(relay_channel | 00).rjust(2, '0')
#     engine.send_did("WRITE", did, send_value)
#     engine.expect_did("WRITE", "开关机E013", "01")
#     engine.wait(1)
#     engine.send_did("READ", "开关机E013", "")
#     engine.expect_did("READ", "开关机E013", "01")
#     engine.wait(1)
#     engine.add_doc_info('监测器检测被测设备的输出端')

# def relay_output_test(did="阀门类型配置E10A", relay_channel=1, output_channel=[0]):
#     """
#     :param did: 控制阀门属性的数据标识
#     :param relay_channel: 控制的设备阀门属性状态
#     :param output_channel: 输出检测接口
#     :return:
#     """
    # send_value = str(relay_channel | 80)
    # if did == "阀门类型配置E10A":
    #     send_value = str(relay_channel | 00).rjust(2, '0')
    # expect_value = str(relay_channel | 00).rjust(2, '0')
    # engine.send_did("WRITE", did, send_value)
    # engine.expect_did("WRITE", "阀门类型配置E10A", expect_value)
    # engine.wait(1)
    # engine.send_did("READ", "阀门类型配置E10A", "")
    # engine.expect_did("READ", "阀门类型配置E10A", expect_value)
    # engine.wait(1)
    # engine.add_doc_info('监测器检测被测设备的输出端')
    # # for channel in output_channel:
    # #     engine.expect_cross_zero_status(channel, 1)
    #
    # send_value = str(relay_channel | 00).rjust(2, '0')
    # engine.send_did("WRITE", did, send_value)
    # engine.expect_did("WRITE", "阀门类型配置E10A", "00")
    # engine.wait(1)
    # engine.send_did("READ", "阀门类型配置E10A", "")
    # engine.expect_did("READ", "阀门类型配置E10A", "00")
    # engine.wait(1)
    # engine.add_doc_info('监测器检测被测设备的输出端')



        
    
# def report_subscribe_expect(devices, write_value="01", expect_value="00", wait_test=True, first_timeout=2,
#                             report_subscribe=True, report_gateway=True, ack=True, scene_type="网关单点控制",
#                             channel=0):
#     """
#     :param devices:订阅者列表
#     :param write_value:写入值
#     :param expect_value:期望值
#     :param report_subscribe:是否上报订阅者，默认为True，表示上报
#     :param first_timeout:状态同步首次上报延时参数
#     :param report_gateway:是否上报网关，默认为True，表示上报
#     :param ack:是否应答，默认为True，表示网关回复；为False时表示网关不回复
#     :param scene_type:场景类型
#     """
#     if scene_type == "网关单点控制":
#         engine.add_doc_info("网关单点控制")
#         engine.send_did("WRITE", "开关机E013", write_value)
#         engine.expect_did("WRITE", "开关机E013", expect_value, timeout=1)
#     elif scene_type == "网关情景模式控制":
#         engine.add_doc_info("网关情景模式控制")
#         # gids=[7, 8, 9, 10, 11]情景模式控制后，第一次上报时间为1.3+0.5*2=2.3s，允许1s误差存在,超时为3.3s
#         engine.send_did("WRITE", "开关机E013", write_value, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
#     elif scene_type == "订阅者01单点控制":
#         engine.add_doc_info("订阅者01单点控制")
#         panel01 = devices[0]
#         panel01.send_did("WRITE", "开关机E013", write_value)
#         panel01.expect_did("WRITE", "开关机E013", expect_value)
#         devices = devices[1:]
#     elif scene_type == "订阅者01情景模式控制":
#         engine.add_doc_info("订阅者01情景模式控制")
#         panel01 = devices[0]
#         # gids=[7, 8, 9, 10, 11]情景模式控制后，第一次上报时间为1.3+0.5*2=2.3s，允许1s误差存在,超时为3.3s
#         panel01.send_did("WRITE", "开关机E013", write_value, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
#     elif scene_type == '本地控制':
#         engine.add_doc_info("本地控制")
#         engine.set_device_sensor_status("按键输入", "短按", channel)
#     else:
#         engine.add_doc_info("操作不再当前允许范围内")
#
#     if report_subscribe:
#         if len(devices) != 0:
#             for i, panel in enumerate(devices):
#                 if i == 0:
#                     panel.expect_did("NOTIFY", "开关机E013", expect_value, timeout=first_timeout)
#                 else:
#                     panel.expect_did("NOTIFY", "开关机E013", expect_value, timeout=2)
#     else:
#         engine.add_doc_info("状态同步不上报订阅者")
#
#     if report_gateway:
#         if report_subscribe:
#             timeout = 2
#         else:
#             timeout = first_timeout
#
#         if scene_type == "网关单点控制":
#             engine.add_doc_info("网关单点控制后，被测设备立即回复，状态同步不再重复上报网关")
#         elif scene_type == "网关情景模式控制":
#             engine.expect_multi_dids("REPORT", "开关机E013", expect_value,
#                                      "导致状态改变的控制设备AIDC01A", config["抄控器默认源地址"], timeout=timeout, ack=ack)
#         elif scene_type == "订阅者01单点控制" or scene_type == "订阅者01情景模式控制":
#             engine.expect_multi_dids("REPORT", "开关机E013", expect_value,
#                                      "导致状态改变的控制设备AIDC01A", panel01.said, timeout=timeout, ack=ack)
#         elif scene_type == '本地控制':
#             engine.expect_multi_dids("REPORT", "开关机E013", expect_value,
#                                      "导致状态改变的控制设备AIDC01A", '00 00 00 00', timeout=timeout, ack=ack)
#         else:
#             engine.add_doc_info("操作不再当前允许范围内")
#     else:
#         engine.add_doc_info("状态同步不上报网关")
#
#     if wait_test:
#         engine.wait(10, allowed_message=False, tips="连续10s未收到被测设备报文，测试正常")
#

# def report_boardcast_expect(devices, write_value="81", expect_value="01", first_timeout=2, scene_type="组地址按位组合"):
#     """
#     :param devices:订阅者列表
#     :param write_value:写入值
#     :param expect_value:期望值
#     :param first_timeout:状态同步首次上报延时参数
#     :param scene_type:场景类型
#     """
#     if scene_type == "组地址按位组合":
#         engine.broadcast_send_multi_dids("WRITE", [7, 8, 9, 10, 11], "BIT1", "通断操作C012", write_value)
#     elif scene_type == "组地址按单字节组合":
#         engine.broadcast_send_multi_dids("WRITE", [7, 8, 9, 10, 11], "U8", "通断操作C012", write_value)
#     elif scene_type == "组地址按双字节组合":
#         engine.broadcast_send_multi_dids("WRITE", [7, 8, 9, 10, 11], "U16", "通断操作C012", write_value)
#     elif scene_type == "存在多个组地址的情况，组地址在前":
#         engine.broadcast_send_multi_dids("WRITE",
#                                          [7, 8, 9, 10, 11], "U8", "通断操作C012", write_value,
#                                          [12, 13, 14, 15, 16], "U8", "通断操作C012", "82",
#                                          [12, 13, 14, 15, 16], "U8", "通断操作C012", "84")
#     elif scene_type == "存在多个组地址的情况，组地址在后":
#         engine.broadcast_send_multi_dids("WRITE",
#                                          [12, 13, 14, 15, 16], "U8", "通断操作C012", "02",
#                                          [12, 13, 14, 15, 16], "U8", "通断操作C012", "04",
#                                          [7, 8, 9, 10, 11], "U8", "通断操作C012", write_value)
#     elif scene_type == "不同组地址混合 按单字节+按双字节+按位组合":
#         engine.broadcast_send_multi_dids("WRITE",
#                                          [7, 8, 9, 10, 11], "BIT1", "通断操作C012", write_value,
#                                          [12, 13, 14, 15, 16], "U8", "通断操作C012", "82",
#                                          [12, 13, 14, 15, 16], "U16", "通断操作C012", "84")
#     elif scene_type == "模拟220字节超长情景模式报文测试":
#         engine.broadcast_send_multi_dids("WRITE",
#                                          [6, 7, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
#                                           180, 181, 182, 183, 184, 185, 186, 187], "U16", "通断操作C012", "88",
#                                          [6, 7,  9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
#                                           180, 181, 182, 183, 184, 185, 186, 187, 188], "U16", "通断操作C012", "84",
#                                          [6, 7,  9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
#                                           180, 181, 182, 183, 184, 185, 186, 187, 188], "U16", "通断操作C012", "82",
#                                          [7, 8, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
#                                           180, 181, 182, 183, 184, 185, 186, 187, 188], "U16", "通断操作C012", write_value)
#     elif scene_type == "sid大于255，组地址按位组合":
#         engine.broadcast_send_multi_dids("WRITE", [220, 230, 250, 280, 289, 290, 291], "BIT1", "通断操作C012", write_value)
#     elif scene_type == "sid大于255，组地址按双字节组合":
#         engine.broadcast_send_multi_dids("WRITE", [220, 230, 250, 280, 289, 290, 291], "U16", "通断操作C012", write_value)
#     else:
#         engine.add_doc_info("不再既定场景测试范围内，请重试")
#
#     if len(devices) != 0:
#         for i, panel in enumerate(devices):
#             if i == 0:
#                 panel.expect_did("NOTIFY", "通断操作C012", expect_value, timeout=first_timeout)
#             else:
#                 panel.expect_did("NOTIFY", "通断操作C012", expect_value)
#     else:
#         engine.add_doc_info("被测设备没有配置订阅者")
#
#     engine.expect_multi_dids("REPORT", "通断操作C012", expect_value,
#                              "导致状态改变的控制设备AIDC01A", config["抄控器默认源地址"], ack=True)
#
#     engine.wait(10, allowed_message=False, tips="本次广播报文测试结束")
#
#
# def return_to_factory():
#     """
#     恢复出厂设置
#     1、发送调试指令FF00，使设备恢复出厂设置
#     此操作恢复出厂设置功能与设备本地按键恢复出厂设置功能相同，清除网关信息，继电器恢复默认状态，其他功能参数恢复至默认，
#     硬件相关的参数或特殊应用参数不清除，如继电器校准参数、继电器动作次数、继电器默认上电状态、背光灯参数；
#     """
#     engine.add_doc_info("发送调试指令，所有的状态和配置参数恢复至出厂参数")
#     engine.report_check_enable_all(True)
#     clear_gw_info()
#     engine.wait(14, allowed_message=False)
#     engine.expect_multi_dids("REPORT",
#                              "通断操作C012", '00',
#                              "导致状态改变的控制设备AIDC01A", config["测试设备地址"], ack=True)
#     engine.report_check_enable_all(False)
#     engine.send_did("WRITE", "自动测试FC00", 密码=config["设备PWD000A"], 自动测试命令="清除系统所有信息")
#     engine.expect_did("WRITE", "自动测试FC00", 密码=config["设备PWD000A"], 自动测试命令="清除系统所有信息")
#     engine.wait(10, tips='预留10s时间供设备清除系统所有信息')