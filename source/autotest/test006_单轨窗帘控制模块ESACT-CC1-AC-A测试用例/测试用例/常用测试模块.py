# encoding:utf-8
# 导入测试引擎
import engine
from autotest.公共用例.public常用测试模块 import *
import time
from engine.spy_device import SpyDevice

config = engine.get_config()


def power_control(init_time=config["被测设备上电后初始化时间"]):
    """
    测试工装控制通断电
    通过控制工装通断，实现给测试设备的通断电，实现断电测试场景
    passed_time 断电重启后设备用时
    """
    from autotest.公共用例.public00init配置初始化 import init_触发设备检测监测器

    engine.add_doc_info("测试工装控制通断电")
    engine.wait(seconds=1, tips='保证和之前的测试存在1s间隔')
    engine.control_relay(0, 0)
    engine.wait(seconds=10, tips='保证被测设备充分断电')
    engine.control_relay(0, 1)

    start_time = time.time()
    engine.wait(seconds=init_time)  # 普通载波设备上电初始化，预留足够时间供载波初始化
    init_触发设备检测监测器()
    passed_time = time.time() - start_time
    engine.add_doc_info('载波设备上电初始化用时{:.3f}秒'.format(passed_time))

    return passed_time


def read_write_test():
    """
    抄读版本及设置参数与查询参数测试，总用时为passed_time

    """
    start_time = time.time()
    engine.wait(1, tips='抄读版本及设置参数、查询参数测试')
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"])
    for value in ['01 00 00', '01 0E 24']:
        engine.send_did("WRITE", "继电器过零点动作延迟时间C020", value)
        engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", value)
        engine.wait(0.5)
        engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
        engine.expect_did("READ", "继电器过零点动作延迟时间C020", value)
        engine.wait(0.5)
    passed_time = time.time() - start_time
    engine.add_doc_info('抄读版本及设置参数、查询参数测试，用时为{:.3f}秒'.format(passed_time))
    return passed_time


def read_default_configuration():
    """
    查询默认参数
    1、出厂状态同步默认为03同时上报设备和网关  主动上报使能标志D005
    2、出厂默认继电器断开延时为1.4ms，闭合延时为3.6ms  继电器过零点动作延迟时间C020
    3、出厂默认行程时间为00 00 00 00  单轨电机窗帘上升下降行程时间0A02
    4、出厂默认保险栓开关状态为00关闭  保险栓开关状态0A06
    5、出厂默认保险栓使能状态为00禁用  保险栓功能使能标识0A30
    6、出厂默认窗帘天空模型使能为00禁用  窗帘天空模型配置0A0A
    7、出厂默认天空模型强制校准次数为30次  窗帘天空模型强制校准次数0A0B
    8、出厂默认窗帘校准后动作次数为0次  窗帘校准后动作次数0A0C
    """
    engine.send_did('READ', '主动上报使能标志D005', '')
    engine.expect_did('READ', '主动上报使能标志D005', '00 03')
    engine.send_did('READ', '继电器过零点动作延迟时间C020', '01')
    engine.expect_did('READ', '继电器过零点动作延迟时间C020', '01 0E 24')
    engine.send_did('READ', '单轨电机窗帘上升下降行程时间0A02', '')
    engine.expect_did('READ', '单轨电机窗帘上升下降行程时间0A02', '00 00 00 00')
    engine.send_did('READ', '保险栓开关状态0A06', '')
    engine.expect_did('READ', '保险栓开关状态0A06', '00')
    engine.send_did('READ', '保险栓功能使能标识0A30', '')
    engine.expect_did('READ', '保险栓功能使能标识0A30', '00')
    engine.send_did('READ', '窗帘天空模型配置0A0A', '')
    engine.expect_did('READ', '窗帘天空模型配置0A0A', '00')
    engine.send_did('READ', '窗帘天空模型强制校准次数0A0B', '')
    engine.expect_did('READ', '窗帘天空模型强制校准次数0A0B', '1E')
    engine.send_did('READ', '窗帘校准后动作次数0A0C', '')
    engine.expect_did('READ', '窗帘校准后动作次数0A0C', '00')


def modify_default_configuration(modify=True, verify=True):
    """
    修改默认参数，使其与默认参数不一致
    """
    if modify:
        engine.add_doc_info('修改参数，使其与默认参数不一致')
        engine.send_did('WRITE', '主动上报使能标志D005', '00 01')
        engine.expect_did('WRITE', '主动上报使能标志D005', '00 01')
        engine.send_did('WRITE', '继电器过零点动作延迟时间C020', '01 20 20')
        engine.expect_did('WRITE', '继电器过零点动作延迟时间C020', '01 20 20')
        engine.send_did('WRITE', '单轨电机窗帘上升下降行程时间0A02', '70 17 70 17')
        engine.expect_did('WRITE', '单轨电机窗帘上升下降行程时间0A02', '70 17 70 17')
        engine.send_did('WRITE', '保险栓开关状态0A06', '01')
        engine.expect_did('WRITE', '保险栓开关状态0A06', '01')
        engine.send_did('WRITE', '保险栓功能使能标识0A30', '01')
        engine.expect_did('WRITE', '保险栓功能使能标识0A30', '01')
        engine.send_did('WRITE', '窗帘天空模型配置0A0A', '01')
        engine.expect_did('WRITE', '窗帘天空模型配置0A0A', '01')
        engine.send_did('WRITE', '窗帘天空模型强制校准次数0A0B', '20')
        engine.expect_did('WRITE', '窗帘天空模型强制校准次数0A0B', '20')

    if verify:
        engine.add_doc_info('验证修改后的参数，确认修改成功')
        engine.send_did('READ', '主动上报使能标志D005', '')
        engine.expect_did('READ', '主动上报使能标志D005', '00 01')
        engine.send_did('READ', '继电器过零点动作延迟时间C020', '01')
        engine.expect_did('READ', '继电器过零点动作延迟时间C020', '01 20 20')
        engine.send_did('READ', '单轨电机窗帘上升下降行程时间0A02', '')
        engine.expect_did('READ', '单轨电机窗帘上升下降行程时间0A02', '70 17 70 17')
        engine.send_did('READ', '保险栓开关状态0A06', '')
        engine.expect_did('READ', '保险栓开关状态0A06', '01')
        engine.send_did('READ', '保险栓功能使能标识0A30', '')
        engine.expect_did('READ', '保险栓功能使能标识0A30', '01')
        engine.send_did('READ', '窗帘天空模型配置0A0A', '')
        engine.expect_did('READ', '窗帘天空模型配置0A0A', '01')
        engine.send_did('READ', '窗帘天空模型强制校准次数0A0B', '')
        engine.expect_did('READ', '窗帘天空模型强制校准次数0A0B', '20')


def return_to_factory():
    """
    恢复出厂设置
    暂不支持调试指令自动测试FC00，通过逐条设置实现恢复出厂设置
    """
    engine.add_doc_info("发送调试指令，所有的状态和配置参数恢复至出厂参数")
    engine.report_check_enable_all(True)
    clear_gw_info()
    engine.wait(14, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "单轨窗帘目标开度0A03", '00',
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], ack=True)
    engine.wait(5)
    engine.report_check_enable_all(False)
    # engine.send_did("WRITE", "自动测试FC00", 密码=config["设备PWD000A"], 自动测试命令="清除系统所有信息")
    # engine.expect_did("WRITE", "自动测试FC00", 密码=config["设备PWD000A"], 自动测试命令="清除系统所有信息")
    # engine.wait(10, tips='预留10s时间供设备清除系统所有信息')
    engine.add_doc_info('暂不支持调试指令自动测试FC00，通过逐条设置实现恢复出厂设置')
    engine.add_doc_info('修改参数，使其与默认参数一致')

    engine.send_did('WRITE', '复位等待时间CD00', '00')
    engine.expect_did('WRITE', '复位等待时间CD00', '00')
    engine.wait(5, tips='通过复位等待时间CD00恢复出厂，预留充足时间')
    engine.add_doc_info('复位等待时间CD00恢复出厂参数，其中继电器过零点动作延迟时间C020属于工装校准参数，不会被清除，'
                        '为了便于后续测试，将该参数设置回默认参数')
    engine.send_did('WRITE', '继电器过零点动作延迟时间C020', '01 0E 24')
    engine.expect_did('WRITE', '继电器过零点动作延迟时间C020', '01 0E 24')


def set_subscriber(name, aid):
    """
    配置订阅者信息
    name :订阅者名称
    aid :订阅者地址
    """
    panel = engine.create_role(name, aid)
    panel.send_did('WRITE', '单轨窗帘目标开度0A03', 开度=0)
    panel.expect_did('WRITE', '单轨窗帘目标开度0A03', 开度=0)
    engine.wait(0.5)
    return panel


def report_power_on_expect(expect_value="00", wait_times=[60], ack=True, wait_enable=True, power_on=True,
                           report_expect=True):
    """
    上电上报测试
    :param expect_value: 期望上报的参数
    :param wait_times: 等待时间列表
    :param ack: 默认为True,应答上报信息；为False时不应答上报信息
    :param wait_enable: 是否进行等待测试，默认为True，验证等待125s，均无其他报文发出。
    :param power_on：默认为True，表示进行断电重启，为False时表示不进行断电重启
    :param report_expect 默认为True，表示进行上报检测，为False时表示不进行上报检测
    """
    if power_on:
        passed_time = power_control()
        if passed_time < wait_times[0]:
            wait_times[0] = wait_times[0] - passed_time
        else:
            engine.add_fail_test('等待时间参数设置错误')
    if report_expect:
        for i, data in enumerate(wait_times):
            ack_action = False
            if i == (len(wait_times) - 1):
                ack_action = ack
            engine.wait((wait_times[i] - 1), allowed_message=False)
            engine.expect_multi_dids("REPORT",
                                     "单轨窗帘目标开度0A03", expect_value,
                                     "单轨窗帘当前开度0A05", expect_value,
                                     '导致状态改变的控制设备AIDC01A', config["测试设备地址"],
                                     ack=ack_action)
    if wait_enable:
        engine.wait(125, allowed_message=False)


def report_subscribe_expect(devices, write_value="32", current_value="00", wait_enable=True, first_timeout=2,
                            report_subscribe=True, report_gateway=True, ack=True, scene_type="网关单点控制", ):
    """
    :param devices:订阅者列表
    :param write_value:写入值
    :param current_value:期望值
    :param wait_enable: 是否进行等待测试，默认为True，验证等待125s，均无其他报文发出。
    :param first_timeout:状态同步首次上报延时参数
    :param report_subscribe:是否上报订阅者，默认为True，表示上报
    :param report_gateway:是否上报网关，默认为True，表示上报
    :param ack:是否应答，默认为True，表示网关回复；为False时表示网关不回复
    :param scene_type:场景类型
    """
    if scene_type == "网关单点控制":
        engine.add_doc_info("网关单点控制")
        engine.send_did('WRITE', '单轨窗帘目标开度0A03', write_value)
        engine.expect_did('WRITE', '单轨窗帘目标开度0A03', write_value)
    elif scene_type == "网关情景模式控制":
        engine.add_doc_info("网关情景模式控制")
        engine.send_did("WRITE", "单轨窗帘目标开度0A03", write_value, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
    elif scene_type == "订阅者01单点控制":
        engine.add_doc_info("订阅者01单点控制")
        panel01 = devices[0]
        panel01.send_did("WRITE", "单轨窗帘目标开度0A03", write_value)
        panel01.expect_did("WRITE", "单轨窗帘目标开度0A03", write_value)
        # devices = devices[1:]
    elif scene_type == "订阅者01情景模式控制":
        engine.add_doc_info("订阅者01情景模式控制")
        panel01 = devices[0]
        panel01.send_did("WRITE", "单轨窗帘目标开度0A03", write_value, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
    else:
        engine.add_doc_info("操作不再当前允许范围内")

    if report_subscribe:
        if len(devices) != 0:
            for i, panel in enumerate(devices):
                if i == 0:
                    timeout = first_timeout
                else:
                    timeout = 2
                panel.expect_multi_dids("NOTIFY",
                                        None, None, "单轨窗帘目标开度0A03", write_value,
                                        None, None, "单轨窗帘当前开度0A05", current_value,
                                        timeout=timeout)

        else:
            engine.add_doc_info('当前模式下没有订阅者')
    else:
        engine.add_doc_info("状态同步不上报订阅者")

    if report_gateway:
        if report_subscribe and len(devices) != 0:
            timeout = 2
        else:
            timeout = first_timeout
        if scene_type == "网关单点控制" or scene_type == "网关情景模式控制":
            if scene_type == "网关单点控制":
                engine.add_doc_info("网关单点控制后，窗帘控制模块状态同步机制与其他设备不一致，仍会上报网关")
            engine.expect_multi_dids("REPORT",
                                     "单轨窗帘目标开度0A03", write_value,
                                     "单轨窗帘当前开度0A05", current_value,
                                     "导致状态改变的控制设备AIDC01A", config["抄控器默认源地址"], timeout=timeout, ack=True)
        elif scene_type == "订阅者01单点控制" or scene_type == "订阅者01情景模式控制":
            engine.expect_multi_dids("REPORT",
                                     "单轨窗帘目标开度0A03", write_value,
                                     "单轨窗帘当前开度0A05", current_value,
                                     "导致状态改变的控制设备AIDC01A", panel01.said, timeout=timeout, ack=True)
        else:
            engine.add_doc_info("操作不再当前允许范围内")
    else:
        engine.add_doc_info("状态同步不上报网关")

    if write_value != current_value:
        engine.add_doc_info('窗帘控制模块的状态同步机制比较特殊，开始被控制后，会立即上报当前开度和目标开度，'
                            '等待窗帘到达目标开度，又会再次上报当前开度和目标开度，所以状态同步测试需要特殊处理')
        if report_subscribe:
            if len(devices) != 0:
                for i, panel in enumerate(devices):
                    if i == 0:
                        timeout = 30
                    else:
                        timeout = 2

                    panel.expect_multi_dids("NOTIFY",
                                            None, None, "单轨窗帘目标开度0A03", write_value,
                                            None, None, "单轨窗帘当前开度0A05", write_value,
                                            timeout=timeout)
            else:
                engine.add_doc_info('当前模式下没有订阅者')
        else:
            engine.add_doc_info("状态同步不上报订阅者")

        if report_gateway:
            if report_subscribe and len(devices) != 0:
                timeout = 2
            else:
                timeout = 30
            if scene_type == "网关单点控制" or scene_type == "网关情景模式控制":
                if scene_type == "网关单点控制":
                    engine.add_doc_info("网关单点控制后，窗帘控制模块状态同步机制与其他设备不一致，仍会上报网关")
                engine.expect_multi_dids("REPORT",
                                         "单轨窗帘目标开度0A03", write_value,
                                         "单轨窗帘当前开度0A05", write_value,
                                         "导致状态改变的控制设备AIDC01A", config["抄控器默认源地址"], timeout=timeout, ack=ack)
            elif scene_type == "订阅者01单点控制" or scene_type == "订阅者01情景模式控制":
                engine.expect_multi_dids("REPORT",
                                         "单轨窗帘目标开度0A03", write_value,
                                         "单轨窗帘当前开度0A05", write_value,
                                         "导致状态改变的控制设备AIDC01A", panel01.said, timeout=timeout, ack=ack)
            else:
                engine.add_doc_info("操作不再当前允许范围内")
        else:
            engine.add_doc_info("状态同步不上报网关")

    if wait_enable:
        engine.wait(10, allowed_message=False, tips="连续10s未收到被测设备报文，测试正常")


def report_broadcast_expect(devices, write_value="81", expect_value="01", first_timeout=2, scene_type="组地址按位组合"):
    """
    :param devices:订阅者列表
    :param write_value:写入值
    :param expect_value:期望值
    :param first_timeout:状态同步首次上报延时参数
    :param scene_type:场景类型
    """
    if scene_type == "组地址按位组合":
        engine.broadcast_send_multi_dids("WRITE", [7, 8, 9, 10, 11], "BIT1", "单轨窗帘目标开度0A03", write_value)
    elif scene_type == "组地址按单字节组合":
        engine.broadcast_send_multi_dids("WRITE", [7, 8, 9, 10, 11], "U8", "单轨窗帘目标开度0A03", write_value)
    elif scene_type == "组地址按双字节组合":
        engine.broadcast_send_multi_dids("WRITE", [7, 8, 9, 10, 11], "U16", "单轨窗帘目标开度0A03", write_value)
    elif scene_type == "存在多个组地址的情况，组地址在前":
        engine.broadcast_send_multi_dids("WRITE",
                                         [7, 8, 9, 10, 11], "U8", "单轨窗帘目标开度0A03", write_value,
                                         [12, 13, 14, 15, 16], "U8", "单轨窗帘目标开度0A03", "82",
                                         [12, 13, 14, 15, 16], "U8", "单轨窗帘目标开度0A03", "84")
    elif scene_type == "存在多个组地址的情况，组地址在后":
        engine.broadcast_send_multi_dids("WRITE",
                                         [12, 13, 14, 15, 16], "U8", "单轨窗帘目标开度0A03", "02",
                                         [12, 13, 14, 15, 16], "U8", "单轨窗帘目标开度0A03", "04",
                                         [7, 8, 9, 10, 11], "U8", "单轨窗帘目标开度0A03", write_value)
    elif scene_type == "不同组地址混合 按单字节+按双字节+按位组合":
        engine.broadcast_send_multi_dids("WRITE",
                                         [7, 8, 9, 10, 11], "BIT1", "单轨窗帘目标开度0A03", write_value,
                                         [12, 13, 14, 15, 16], "U8", "单轨窗帘目标开度0A03", "82",
                                         [12, 13, 14, 15, 16], "U16", "单轨窗帘目标开度0A03", "84")
    elif scene_type == "模拟220字节超长情景模式报文测试":
        engine.broadcast_send_multi_dids("WRITE",
                                         [6, 7, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
                                          180, 181, 182, 183, 184, 185, 186, 187], "U16", "单轨窗帘目标开度0A03", "88",
                                         [6, 7, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
                                          180, 181, 182, 183, 184, 185, 186, 187, 188], "U16", "单轨窗帘目标开度0A03", "84",
                                         [6, 7, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
                                          180, 181, 182, 183, 184, 185, 186, 187, 188], "U16", "单轨窗帘目标开度0A03", "82",
                                         [7, 8, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
                                          180, 181, 182, 183, 184, 185, 186, 187, 188], "U16", "单轨窗帘目标开度0A03",
                                         write_value)
    elif scene_type == "sid大于255，组地址按位组合":
        engine.broadcast_send_multi_dids("WRITE", [220, 230, 250, 280, 289, 290, 291], "BIT1", "单轨窗帘目标开度0A03",
                                         write_value)
    elif scene_type == "sid大于255，组地址按双字节组合":
        engine.broadcast_send_multi_dids("WRITE", [220, 230, 250, 280, 289, 290, 291], "U16", "单轨窗帘目标开度0A03",
                                         write_value)
    else:
        engine.add_doc_info("不再既定场景测试范围内，请重试")

    if len(devices) != 0:
        for i, panel in enumerate(devices):
            if i == 0:
                panel.expect_did("NOTIFY", "单轨窗帘目标开度0A03", expect_value, timeout=first_timeout)
            else:
                panel.expect_did("NOTIFY", "单轨窗帘目标开度0A03", expect_value)
    else:
        engine.add_doc_info("被测设备没有配置订阅者")

    engine.expect_multi_dids("REPORT", "单轨窗帘目标开度0A03", expect_value,
                             "导致状态改变的控制设备AIDC01A", config["抄控器默认源地址"], ack=True)

    engine.wait(10, allowed_message=False, tips="本次广播报文测试结束")
