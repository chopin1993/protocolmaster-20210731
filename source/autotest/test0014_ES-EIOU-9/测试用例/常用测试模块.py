# encoding:utf-8
# 导入测试引擎
import engine
from autotest.公共用例.public常用测试模块 import *
import time

from protocol import Smart7eProtocol

config = engine.get_config()


def relay_output_test(did="通断操作C012", relay_channel=1, output_channel=[0]):
    """
    :param did: 控制继电器的数据标识
    :param relay_channel: 控制的设备通道
    :param output_channel: 输出检测接口
    :return:
    """
    send_value = str(relay_channel | 80)
    if did == "继电器翻转C018":
        send_value = str(relay_channel | 00).rjust(2, '0')
    expect_value = str(relay_channel | 00).rjust(2, '0')
    engine.send_did("WRITE", did, send_value)
    engine.expect_did("WRITE", "通断操作C012", expect_value)
    engine.wait(1)
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", expect_value)
    engine.add_doc_info('监测器检测被测设备的输出端')
    for channel in output_channel:
        engine.expect_cross_zero_status(channel, 1)

    send_value = str(relay_channel | 00).rjust(2, '0')
    engine.send_did("WRITE", did, send_value)
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(1)
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")
    engine.add_doc_info('监测器检测被测设备的输出端')
    for channel in output_channel:
        engine.expect_cross_zero_status(channel, 0)


def read_write_test():
    """
    抄读版本及控制通断测试，用时为passed_time

    """
    start_time = time.time()
    engine.wait(1, tips='抄读版本及控制通断测试')
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"])
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(0.5)
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(1)
    engine.send_did("READ", "通断操作C012")
    engine.expect_did("READ", "通断操作C012", "00")
    # engine.expect_multi_dids("REPORT",
    #                          "通断操作C012", "00", "亮度值C0A2", "01 ** **", "亮度值C0A2", "02 ** **",
    #                          "导致状态改变的控制设备AIDC01A", config["抄控器默认源地址"], ack=True)
    passed_time = time.time() - start_time
    engine.add_doc_info('抄读版本及控制通断测试，用时为{:.3f}秒'.format(passed_time))
    return passed_time


def set_subscriber(name, aid):
    """
    配置订阅者信息
    name :订阅者名称
    aid :订阅者地址
    """
    panel = engine.create_role(name, aid)

    engine.add_doc_info('**********操作设备继电器翻转-01**********')
    panel.send_did("WRITE", "继电器翻转C018", "81")
    panel.expect_did("WRITE", "通断操作C012", "**")
    engine.wait(1.6)  # 操作后1.5s后上报状态2条，
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", '**', "亮度值C0A2", "01 ** **", "亮度值C0A2", "02 ** **")  # 订阅者上报无需回复,ack=F
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", '**', "亮度值C0A2", "01 ** **", "亮度值C0A2", "02 ** **",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"])  # 订阅者上报无需回复，ack=F

    engine.add_doc_info('-->操作设备继电器翻转-02<--')
    panel.send_did("WRITE", "继电器翻转C018", "81")
    panel.expect_did("WRITE", "通断操作C012", "**")  # 回复报文，之后设备再上报两条，间隔
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", '**', "亮度值C0A2", "01 ** **", "亮度值C0A2", "02 ** **")  # 订阅者上报无需回复,ack=F
    engine.wait(1.6)  # 等待调光最终状态上上报
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", '**', "亮度值C0A2", "01 ** **", "亮度值C0A2", "02 ** **",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"])  # 订阅者上报无需回复，ack=F
    return panel


def report_gateway_expect(expect_value="00", wait_times=[15], ack=True, quit_net=False, wait_enable=True):
    """
    添加上报测试
    :param wait_enable:
    :param wait_times:等待时间列表,自定义
    :param expect_value:期望上报的参数
    :param ack:默认为True,应答上报信息；为False时不应答上报信息
    :param quit_net:退网参数，默认为False，不发送退网指令，为True时，发送退网指令
    """
    set_gw_info()  # 设置网关PANID信息，模拟设备入网
    # 定义添加上报
    for i, wait_time in enumerate(wait_times):  # 15s后检查入网上报信息;10s,100s后检测上报重发；
        if i != (len(wait_times) - 1):
            ack_action = False
        else:
            ack_action = ack
        engine.wait((wait_time - 1), allowed_message=False)  # 打印等待时间，倒计时
        engine.expect_multi_dids("REPORT",
                                 "通断操作C012", expect_value, "亮度值C0A2", "01 ** **", "亮度值C0A2", "02 ** **",
                                 "导致状态改变的控制设备AIDC01A", config["测试设备地址"], ack=ack_action)  # 本设备入网上报的期待值，只关心关心数据标识不关心数据本身
        # engine.wait(1.5)
        # engine.expect_multi_dids("REPORT",
        #                          "通断操作C012", expect_value, "亮度值C0A2", "01 ** **", "亮度值C0A2", "02 ** **",
        #                          "导致状态改变的控制设备AIDC01A", config["测试设备地址"], ack=ack_action) # 调光控制上报两次（目标，当前）
    if wait_enable:  # 等待125s，检查设备上报之后，应不在有此报文
        engine.wait(125, allowed_message=False)
    if quit_net:
        engine.send_did("WRITE", "退网通知060B", 退网设备=config["测试设备地址"])


def report_power_on_expect(expect_value="00", wait_times=[60], ack=True, wait_enable=True):
    """
    上电上报测试
    :param wait_enable:
    :param expect_value: 期望上报的参数；
    :param wait_times: 等待时间列表；
    :param ack: 默认为True,应答上报信息；为False时不应答上报信息；
    """
    passed_time = power_control()
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
                                 "通断操作C012", expect_value, "亮度值C0A2", "01 ** **", "亮度值C0A2", "02 ** **",
                                 "导致状态改变的控制设备AIDC01A", config["测试设备地址"], ack=ack_action)
    if wait_enable:
        engine.wait(125, allowed_message=False)


def report_subscribe_expect(devices, write_value="81", expect_value="01", wait_test=True, first_timeout=2,
                            report_subscribe=True, report_gateway=True, ack=True, scene_type="网关单点控制",
                            channel=0):
    """
    :param wait_test:
    :param channel:
    :param devices:订阅者列表
    :param write_value:写入值
    :param expect_value:期望值
    :param report_subscribe:是否上报订阅者，默认为True，表示上报
    :param first_timeout:状态同步首次上报延时参数
    :param report_gateway:是否上报网关，默认为True，表示上报
    :param ack:是否应答，默认为True，表示网关回复；为False时表示网关不回复
    :param scene_type:场景类型
    """
    if scene_type == "网关单点控制":
        engine.add_doc_info("网关单点控制-01")
        engine.send_did("WRITE", "通断操作C012", write_value)
        engine.expect_did("WRITE", "通断操作C012", expect_value, timeout=2)
        # engine.expect_multi_dids("REPORT",
        #                          "通断操作C012", '**', "亮度值C0A2", "01 ** **", "亮度值C0A2", "02 ** **",
        #                          ack=True, timeout=2)  # 设备可靠上报2条,
        # engine.expect_multi_dids("REPORT",
        #                          "通断操作C012", '**', "亮度值C0A2", "01 ** **", "亮度值C0A2", "02 ** **",
        #                          ack=True, timeout=2)  # 设备可靠上报2条
    elif scene_type == "网关情景模式控制":
        engine.add_doc_info("网关情景模式控制")
        # gids=[7, 8, 9, 10, 11]情景模式控制后，第一次上报时间为1.3+0.5*2=2.3s，允许1s误差存在,超时为3.3s
        engine.send_did("WRITE", "通断操作C012", write_value, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
        for i in range(2):
            engine.expect_multi_dids("REPORT",
                                     "通断操作C012", '00', "亮度值C0A2", "01 ** **", "亮度值C0A2", "02 ** **",
                                     "导致状态改变的控制设备AIDC01A", config["测试设备地址"], ack=True, timeout=4)  # 设备可靠上报两条

    elif scene_type == "订阅者01单点控制":
        engine.add_doc_info("订阅者01单点控制")
        panel01 = devices[0]
        panel01.send_did("WRITE", "通断操作C012", write_value)
        panel01.expect_did("WRITE", "通断操作C012", expect_value)
        for i in range(0, 2, 1):
            engine.expect_multi_dids("REPORT",
                                     "通断操作C012", '00', "亮度值C0A2", "01 ** **", "亮度值C0A2", "02 ** **",
                                     "导致状态改变的控制设备AIDC01A", config["测试设备地址"], ack=False, timeout=6)
        devices = devices[1:]
    elif scene_type == "订阅者01情景模式控制":
        engine.add_doc_info("订阅者01情景模式控制")  # 设备无回复
        panel01 = devices[0]
        # gids=[7, 8, 9, 10, 11]情景模式控制后，第一次上报时间为1.3+0.5*2=2.3s，允许1s误差存在,超时为3.3s
        panel01.send_did("WRITE", "通断操作C012", write_value, gids=[7, 8, 9, 10, 11], gid_type="BIT1")  # 本条无回复
        for i in range(0, 2, 1):
            engine.expect_multi_dids("REPORT",
                                     "通断操作C012", '00', "亮度值C0A2", "01 ** **", "亮度值C0A2", "02 ** **",
                                     "导致状态改变的控制设备AIDC01A", config["测试设备地址"], ack=False, timeout=6)  # 无需回复
    elif scene_type == '本地控制':
        engine.add_doc_info("本地控制")
        engine.set_device_sensor_status("按键输入", "短按", channel)
        for i in range(0, 2, 1):
            engine.expect_multi_dids("REPORT",
                                     "通断操作C012", '00', "亮度值C0A2", "01 ** **", "亮度值C0A2", "02 ** **",
                                     "导致状态改变的控制设备AIDC01A", config["测试设备地址"], ack=False, timeout=6)  # 无需回复
    else:
        engine.add_doc_info("操作不再当前允许范围内")

    if report_subscribe:
        if len(devices) != 0:
            for i, panel in enumerate(devices):
                if i == 0:
                    panel.expect_did("NOTIFY", "通断操作C012", expect_value, timeout=first_timeout)
                else:
                    panel.expect_did("NOTIFY", "通断操作C012", expect_value, timeout=2)
    else:
        engine.add_doc_info("状态同步不上报订阅者")

    if report_gateway:
        if report_subscribe:
            timeout = 2
        else:
            timeout = first_timeout

        if scene_type == "网关单点控制":
            engine.add_doc_info("网关进行了单点控制")
            # engine.expect_multi_dids("REPORT",
            #                          "通断操作C012", '**', "亮度值C0A2", "01 ** **", "亮度值C0A2", "02 ** **",
            #                          ack=True, timeout=1)
        elif scene_type == "网关情景模式控制":
            engine.expect_multi_dids("REPORT", "通断操作C012", '**', "亮度值C0A2", "01 ** **", "亮度值C0A2", "02 ** **",
                                     "导致状态改变的控制设备AIDC01A", config["抄控器默认源地址"], timeout=timeout, ack=ack)
            for i in range(0, 2, 1):
                engine.expect_multi_dids("REPORT",
                                         "通断操作C012", '**', "亮度值C0A2", "01 ** **", "亮度值C0A2", "02 ** **",
                                         "导致状态改变的控制设备AIDC01A", config["测试设备地址"], ack=True, timeout=4)  # 设备可靠上报两条
        elif scene_type == "订阅者01单点控制" or scene_type == "订阅者01情景模式控制":
            for i in range(0, 2, 1):
                engine.expect_multi_dids("REPORT",
                                         "通断操作C012", '**', "亮度值C0A2", "01 ** **", "亮度值C0A2", "02 ** **",
                                         "导致状态改变的控制设备AIDC01A", config["测试设备地址"], ack=False, timeout=6)
        elif scene_type == '本地控制':
            for i in range(0, 2, 1):
                engine.expect_multi_dids("REPORT",
                                         "通断操作C012", '**', "亮度值C0A2", "01 ** **", "亮度值C0A2", "02 ** **",
                                         "导致状态改变的控制设备AIDC01A", config["测试设备地址"], ack=False, timeout=6)
        else:
            engine.add_doc_info("操作不再当前允许范围内")
    else:
        engine.add_doc_info("状态同步不上报网关")

    if wait_test:
        engine.wait(10, allowed_message=False, tips="连续10s未收到被测设备报文，测试正常")


def report_boardcast_expect(devices, write_value="81", expect_value="01", first_timeout=2, scene_type="组地址按位组合"):
    """
    :param devices:订阅者列表
    :param write_value:写入值
    :param expect_value:期望值
    :param first_timeout:状态同步首次上报延时参数
    :param scene_type:场景类型
    """
    if scene_type == "组地址按位组合":
        engine.broadcast_send_multi_dids("WRITE", [7, 8, 9, 10, 11], "BIT1", "通断操作C012", write_value)
    elif scene_type == "组地址按单字节组合":
        engine.broadcast_send_multi_dids("WRITE", [7, 8, 9, 10, 11], "U8", "通断操作C012", write_value)
    elif scene_type == "组地址按双字节组合":
        engine.broadcast_send_multi_dids("WRITE", [7, 8, 9, 10, 11], "U16", "通断操作C012", write_value)
    elif scene_type == "存在多个组地址的情况，组地址在前":
        engine.broadcast_send_multi_dids("WRITE",
                                         [7, 8, 9, 10, 11], "U8", "通断操作C012", write_value,
                                         [12, 13, 14, 15, 16], "U8", "通断操作C012", "82",
                                         [12, 13, 14, 15, 16], "U8", "通断操作C012", "84")
    elif scene_type == "存在多个组地址的情况，组地址在后":
        engine.broadcast_send_multi_dids("WRITE",
                                         [12, 13, 14, 15, 16], "U8", "通断操作C012", "02",
                                         [12, 13, 14, 15, 16], "U8", "通断操作C012", "04",
                                         [7, 8, 9, 10, 11], "U8", "通断操作C012", write_value)
    elif scene_type == "不同组地址混合 按单字节+按双字节+按位组合":
        engine.broadcast_send_multi_dids("WRITE",
                                         [7, 8, 9, 10, 11], "BIT1", "通断操作C012", write_value,
                                         [12, 13, 14, 15, 16], "U8", "通断操作C012", "82",
                                         [12, 13, 14, 15, 16], "U16", "通断操作C012", "84")
    elif scene_type == "模拟220字节超长情景模式报文测试":
        engine.broadcast_send_multi_dids("WRITE",
                                         [6, 7, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
                                          180, 181, 182, 183, 184, 185, 186, 187], "U16", "通断操作C012", "88",
                                         [6, 7, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
                                          180, 181, 182, 183, 184, 185, 186, 187, 188], "U16", "通断操作C012", "84",
                                         [6, 7, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
                                          180, 181, 182, 183, 184, 185, 186, 187, 188], "U16", "通断操作C012", "82",
                                         [7, 8, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
                                          180, 181, 182, 183, 184, 185, 186, 187, 188], "U16", "通断操作C012", write_value)
    elif scene_type == "sid大于255，组地址按位组合":
        engine.broadcast_send_multi_dids("WRITE", [220, 230, 250, 280, 289, 290, 291], "BIT1", "通断操作C012", write_value)
    elif scene_type == "sid大于255，组地址按双字节组合":
        engine.broadcast_send_multi_dids("WRITE", [220, 230, 250, 280, 289, 290, 291], "U16", "通断操作C012", write_value)
    else:
        engine.add_doc_info("不再既定场景测试范围内，请重试")

    if len(devices) != 0:
        for i, panel in enumerate(devices):
            if i == 0:
                panel.expect_did("NOTIFY", "通断操作C012", expect_value, timeout=first_timeout)
            else:
                panel.expect_did("NOTIFY", "通断操作C012", expect_value)
    else:
        engine.add_doc_info("被测设备没有配置订阅者")

    engine.expect_multi_dids("REPORT", "通断操作C012", expect_value,
                             "导致状态改变的控制设备AIDC01A", config["抄控器默认源地址"], ack=True)

    engine.wait(10, allowed_message=False, tips="本次广播报文测试结束")


def return_to_factory():
    """
    恢复出厂设置
    1、发送调试指令FF00，使设备恢复出厂设置
    此操作恢复出厂设置功能与设备本地按键恢复出厂设置功能相同，清除网关信息，继电器恢复默认状态，其他功能参数恢复至默认，
    硬件相关的参数或特殊应用参数不清除，如继电器校准参数、继电器动作次数、继电器默认上电状态、背光灯参数；
    """
    engine.add_doc_info("发送调试指令，所有的状态和配置参数恢复至出厂参数")
    engine.report_check_enable_all(True)
    clear_gw_info()
    engine.wait(14, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", '00', "亮度值C0A2", "01 ** **", "亮度值C0A2", "02 ** **",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], ack=True)
    engine.report_check_enable_all(False)
    engine.send_did("WRITE", "自动测试FC00", 密码=config["设备PWD000A"], 自动测试命令="清除系统所有信息")
    engine.expect_did("WRITE", "自动测试FC00", 密码=config["设备PWD000A"], 自动测试命令="清除系统所有信息")
    engine.wait(10, tips='预留10s时间供设备清除系统所有信息')


def twice_report_chack(channel=1):  # 试验代码
    """
    检测两次上报
        -当前亮度！=目标亮度；
        -当前亮度=目标亮度；
    :param channel:1或2
    :return:
    """

    def check_twice():
        """
        检测两次上报
        :return:
        """
        channel_dict = {'01': '01 ** **', '02': '02 ** **'}
        for i in range(2):  # 设将上报两条
            engine.expect_multi_dids("REPORT",
                                     "通断操作C012", '00', "亮度值C0A2", channel_dict['01'], "亮度值C0A2", channel_dict['02'],
                                     "导致状态改变的控制设备AIDC01A", config["测试设备地址"], ack=False)
            engine.wait(0.3)

    if channel == 1:
        check_twice()
    elif channel == 2:
        check_twice()
    else:
        engine.add_doc_info('输入了不存在的通道号！')


def back_devices():
    """
    恢复设备专状态
    :return:
    """
    engine.send_did('WRITE', '查询设置超温保护温度上限C0A5', '02 64')
    engine.expect_did('WRITE', '查询设置超温保护温度上限C0A5', '02 64')
    engine.send_did('WRITE', '查询设置超温保护温度上限C0A5', '01 64')
    engine.expect_did('WRITE', '查询设置超温保护温度上限C0A5', '01 64')
    engine.wait(2, tips='等待设备恢复')
    engine.send_did('WRITE', '亮度值C0A2', '02 00')
    engine.expect_did('WRITE', '亮度值C0A2', '02 00 **')
    engine.send_did('WRITE', '亮度值C0A2', '01 00')
    engine.expect_did('WRITE', '亮度值C0A2', '01 00 **')


def choice_temp_test_type(type=None):
    """

    :param type:
    :return:
    """
    type_list = [20, 21, 22, 23, 24, 25]
    if type == type_list[0]:
        engine.add_doc_info('配置为NTC10K-3435(0x20)输入模式')
        engine.send_FE02_did('WRITE', 'IO配置D201', '01 20 02 20 03 20 04 20 05 20 06 20 07 20 08 20 09 20')
        engine.expect_FE02_did('WRITE', 'IO配置D201', '01 20 02 20 03 20 04 20 05 20 06 20 07 20 08 20 09 20')
    elif type == type_list[1]:
        engine.add_doc_info('配置为NTC10K-3950(0x21)输入模式')
        engine.send_FE02_did('WRITE', 'IO配置D201', '01 21 02 21 03 21 04 21 05 21 06 21 07 21 08 21 09 21')
        engine.expect_FE02_did('WRITE', 'IO配置D201', '01 20 02 20 03 20 04 20 05 20 06 20 07 20 08 20 09 20')
    elif type == type_list[2]:
        engine.add_doc_info('配置为PT1000(0x22)输入模式')
        engine.send_FE02_did('WRITE', 'IO配置D201', '01 22 02 22 03 22 04 22 05 22 06 22 07 22 08 22 09 22')
        engine.expect_FE02_did('WRITE', 'IO配置D201', '01 22 02 22 03 22 04 22 05 22 06 22 07 22 08 22 09 22')
    elif type == type_list[3]:
        engine.add_doc_info('配置为NI1000(0x23)输入模式')
        engine.send_FE02_did('WRITE', 'IO配置D201', '01 23 02 23 03 23 04 23 05 23 06 23 07 23 08 23 09 23')
        engine.expect_FE02_did('WRITE', 'IO配置D201', '01 23 02 23 03 23 04 23 05 23 06 23 07 23 08 23 09 23')
    elif type == type_list[4]:
        engine.add_doc_info('配置为NTC20K-3950(0x24)输入模式')
        engine.send_FE02_did('WRITE', 'IO配置D201', '01 24 02 24 03 24 04 24 05 24 06 24 07 24 08 24 09 24')
        engine.expect_FE02_did('WRITE', 'IO配置D201', '01 24 02 24 03 24 04 24 05 24 06 24 07 24 08 24 09 24')
    else:   # type == 25
        engine.add_doc_info('配置为NTC100K-3950(0x25)输入模式')
        engine.send_FE02_did('WRITE', 'IO配置D201', '01 25 02 25 03 25 04 25 05 25 06 25 07 25 08 25 09 25')
        engine.expect_FE02_did('WRITE', 'IO配置D201', '01 25 02 25 03 25 04 25 05 25 06 25 07 25 08 25 09 25')


def ctrl_relay_open(channel):
    """
    EIOU-控制工装对应继电器，开
    :param channel:工装上的继电器通道号
    :return:
    """
    if len(str(channel)) == 1:
        engine.send_did('WRITE', '22V通断电FE04', '01 '+'0'+str(channel))
        engine.expect_did('WRITE', '22V通断电FE04', '01 '+'0'+str(channel))
    else:   # len(str(channel)) == 2
        engine.send_did('WRITE', '22V通断电FE04', '01 '+str(channel))
        engine.expect_did('WRITE', '22V通断电FE04', '01 '+str(channel))


def ctrl_relay_close(channel):
    """
    EIOU-控制工装对应继电器，关
    :param channel:工装上的继电器通道号
    :return:
    """
    if len(str(channel)) == 1:
        engine.send_did('WRITE', '22V通断电FE04', '00 ' + '0' + str(channel))
        engine.expect_did('WRITE', '22V通断电FE04', '00 ' + '0' + str(channel))
    else:   # len(str(channel)) == 2
        engine.send_did('WRITE', '22V通断电FE04', '00 ' + str(channel))
        engine.expect_did('WRITE', '22V通断电FE04', '00 ' + str(channel))


# def read_FE06_date(data_type):
#     """
#     工装数据读取：
#     TT数据类型=> 0x01:DO正压数据读取；
#             0x02:DO负压数据读取；
#             0x03:AI电压数据读取；
#             0x04:AI电流数据读取；
#             0x05:AI电阻数据读取；
#     工装回复数据格式:TT+XX;
#         对于DO类型，XX为1Byte；XX-0x01输出控制有正压/负压，XX-0x00输出控制无正压/负压；
#         对于AI类型，XX为5Byte；BCD小端表示；
#     :param data_type:
#     :return:
#     """
#     engine.send_did('READ', '工装数据读取FE06', '0'+str(data_type))
#     engine.wait(1, tips='等待工装回复')
#     engine.expect_did('READ', '工装数据读取FE06', '0'+str(data_type), "00")     # 取得的数据稍有差别


def get_rcv_msg_date(msg):
    """
    获取设备回复报文中的数据
    :param msg: 收到的except报文
    :return:
    """
    protocol = Smart7eProtocol()
    (found, start, length) = protocol.find_frame_in_buff(msg.data)
    if found:
        frame_data = msg.data[start:start + length]
        first = frame_data[-6:-2][::-1]     # 报文中倒数-2到-6位是电阻数据
        reversed_data = []
        for raw_data in first:
            if raw_data <= 9:
                reversed_data.append('0' + str(raw_data))
            else:  # raw_data > 9:
                reversed_data.append(str(raw_data))
        rcv_msg_date = reversed_data[0] + reversed_data[1] + reversed_data[2] + reversed_data[3]
        rcv_msg_date = int(rcv_msg_date)
        return rcv_msg_date
