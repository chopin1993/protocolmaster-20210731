# encoding:utf-8
# 导入测试引擎
import engine
from autotest.公共用例.public常用测试模块 import *

config = engine.get_config()


def read_write_test():
    """
    抄读版本及控制通断测试，用时约3s
    """
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"])
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(1)
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(1)
    engine.send_did("READ", "通断操作C012")
    engine.expect_did("READ", "通断操作C012", "00")


def set_baud_rate(bps=9600):
    """
    设置抄控器的波特率
    :param bps:
    """
    if bps == 9600:
        engine.add_doc_info('将当前的串口波特率设置为9600')
        engine.send_local_msg("设置串口波特率", '02 00')  # 9600bps
        engine.expect_local_msg("确认")
        config["波特率"] = "9600"
    elif bps == 115200:
        engine.add_doc_info('将当前的串口波特率设置为115200')
        engine.send_local_msg("设置串口波特率", '04 00')  # 115200bps
        engine.expect_local_msg("确认")
        config["波特率"] = "115200"


def set_subscriber(name, aid):
    """
    配置订阅者信息
    name :订阅者名称
    aid :订阅者地址
    """
    panel = engine.create_role(name, aid)
    panel.send_did("WRITE", "通断操作C012", "81")
    panel.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(0.5)
    panel.send_did("WRITE", "通断操作C012", "01")
    panel.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(0.5)
    return panel


def report_gateway_expect(expect_value="00", wait_times=[15], ack=True, quit_net=False):
    """
    :param wait_times:等待时间列表,自定义多个等待时间
    :param expect_value:期望上报的参数
    :param ack:默认为True,应答上报信息；为False时不应答上报信息
    :param quit_net:退网参数，默认为False，不发送退网指令，为True时，发送退网指令
    """
    set_gw_info()  # 设置网关PANID信息，模拟设备入网
    # 定义添加上报
    for i, time_out in enumerate(wait_times):
        ack = False
        if i == (len(wait_times) - 1):
            ack = ack
        engine.wait((time_out - 1), allowed_message=False)
        engine.expect_multi_dids("REPORT",
                                     '日期C010','',
                                     '时刻C011','',
                                     "通断操作C012", expect_value,
                                     "导致状态改变的控制设备AIDC01A", config["测试设备地址"],
                                     '模式上报FC41','02',
                                     '设置语言FC34','00',
                                     '通电时间读取和设定C340','00 01 08 00 20 00',
                                     '时段使能C341','00',
                                     '读传感器数据B701','17 01',
                                     ack=ack)
    engine.wait(125, allowed_message=False)
    if quit_net:
        engine.send_did("WRITE", "退网通知060B", 退网设备=config["测试设备地址"])


def report_power_on_expect(panid=config["panid"], sid=8, expect_value="00", wait_time=[15], ack=True):
    """
    :param panid:
    :param sid:
    :param expect_value:
    :param wait_time:
    :param ack:
    """
    set_gw_info(panid=panid, sid=sid)
    engine.wait(14, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             '日期C010', '',
                             '时刻C011', '',
                             "通断操作C012", expect_value,
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"],
                             '模式上报FC41', '02',
                             '设置语言FC34', '00',
                             '通电时间读取和设定C340', '00 01 08 00 20 00',
                             '时段使能C341', '00',
                             '读传感器数据B701', '17 01',
                             ack=True)
    set_gw_info(panid=panid, sid=1, aid=config["前置通断电工装AID"], pw=config["前置通断电工装PWD"])

    power_control(time=0)

    for i, data in enumerate(wait_time):
        if i != (len(wait_time) - 1):
            engine.wait((wait_time[i] - 1), allowed_message=False)
            engine.expect_multi_dids("REPORT",
                                     '日期C010','',
                                     '时刻C011','',
                                     "通断操作C012", expect_value,
                                     "导致状态改变的控制设备AIDC01A", config["测试设备地址"],
                                     '模式上报FC41','02',
                                     '设置语言FC34','00',
                                     '通电时间读取和设定C340','00 01 08 00 20 00',
                                     '时段使能C341','00',
                                     '读传感器数据B701','17 01'
                                     )
        else:
            engine.wait((wait_time[i] - 1), allowed_message=False)
            engine.expect_multi_dids("REPORT",
                                     '日期C010','',
                                     '时刻C011','',
                                     "通断操作C012", expect_value,
                                     "导致状态改变的控制设备AIDC01A", config["测试设备地址"],
                                     '模式上报FC41','02',
                                     '设置语言FC34','00',
                                     '通电时间读取和设定C340','00 01 08 00 20 00',
                                     '时段使能C341','00',
                                     '读传感器数据B701','17 01',
                                     ack=ack)

    engine.wait(125, allowed_message=False)


def report_subscribe_expect(devices, write_value="01", expect_value="00", report_subscribe=True, wait_test=True,
                            first_timeout=2, report_gateway=True, ack=True, scene_type="网关单点控制"):
    """
    :param devices:订阅者列表
    :param write_value:写入值
    :param expect_value:期望值
    :param report_subscribe:是否上报订阅者，默认为True，表示上报
    :param first_timeout:状态同步首次上报延时参数
    :param report_gateway:是否上报网关，默认为True，表示上报
    :param ack:是否应答，默认为True，表示网关回复；为False时表示网关不回复
    :param scene_type:场景类型
    """
    config = engine.get_config()
    if scene_type == "网关单点控制":
        engine.add_doc_info("网关单点控制")
        engine.send_did("WRITE", "通断操作C012", write_value)
        engine.expect_did("WRITE", "通断操作C012", expect_value)
    elif scene_type == "网关情景模式控制":
        engine.add_doc_info("网关情景模式控制")
        # gids=[7, 8, 9, 10, 11]情景模式控制后，第一次上报时间为1.3+0.5*2=2.3s，允许1s误差存在,超时为3.3s
        engine.send_did("WRITE", "通断操作C012", write_value, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
    elif scene_type == "订阅者01单点控制":
        engine.add_doc_info("订阅者01单点控制")
        panel01 = devices[0]
        panel01.send_did("WRITE", "通断操作C012", write_value)
        panel01.expect_did("WRITE", "通断操作C012", expect_value)
        devices = devices[1:]
    elif scene_type == "订阅者01情景模式控制":
        engine.add_doc_info("订阅者01情景模式控制")
        panel01 = devices[0]
        # gids=[7, 8, 9, 10, 11]情景模式控制后，第一次上报时间为1.3+0.5*2=2.3s，允许1s误差存在,超时为3.3s
        panel01.send_did("WRITE", "通断操作C012", write_value, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
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
            engine.add_doc_info("网关单点控制后，被测设备立即回复，状态同步不再重复上报网关")
        elif scene_type == "网关情景模式控制":
            engine.expect_multi_dids("REPORT",
                                     "通断操作C012", expect_value,
                                     "导致状态改变的控制设备AIDC01A", config["抄控器默认源地址"],
                                     timeout=timeout, ack=ack)
        elif scene_type == "订阅者01单点控制" or scene_type == "订阅者01情景模式控制":
            engine.expect_multi_dids("REPORT",
                                     "通断操作C012", expect_value,
                                     "导致状态改变的控制设备AIDC01A", panel01.said,
                                     timeout=timeout, ack=ack)
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
                                         [7, 8, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
                                          180, 181, 182, 183, 184, 185, 186, 187], "U16", "通断操作C012", "88",
                                         [7, 8, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
                                          180, 181, 182, 183, 184, 185, 186, 187, 188], "U16", "通断操作C012", "84",
                                         [7, 8, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
                                          180, 181, 182, 183, 184, 185, 186, 187, 188], "U16", "通断操作C012", "82",
                                         [7, 8, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
                                          180, 181, 182, 183, 184, 185, 186, 187, 188], "U16", "通断操作C012", write_value)
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

    engine.expect_multi_dids("REPORT",
                             "通断操作C012", expect_value,
                             "导致状态改变的控制设备AIDC01A", config["抄控器默认源地址"],
                             ack=True)

    engine.wait(10, allowed_message=False, tips="本次广播报文测试结束")
