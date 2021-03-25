# encoding:utf-8
# 导入测试引擎
import engine
from autotest.公共用例.public常用测试模块 import *
import time

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
    # init_触发设备检测监测器()
    passed_time = time.time() - start_time
    engine.add_doc_info('载波设备上电初始化用时{:.3f}秒'.format(passed_time))

    return passed_time


def read_write_test():
    """
    抄读版本及设置参数与查询参数测试，总用时为passed_time

    """
    start_time = time.time()
    engine.wait(1, tips='抄读版本及设置参数与查询参数测试')
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"])
    for value in [60, 5]:
        engine.send_did('WRITE', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=value)
        engine.expect_did('WRITE', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=value)
        engine.wait(0.5)
        engine.send_did('READ', '上报间隔设置D004', 传感器类型='人体红外移动')
        engine.expect_did('READ', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=value)
        engine.wait(0.5)
    passed_time = time.time() - start_time
    engine.add_doc_info('抄读版本及设置参数与查询参数测试，用时为{:.3f}秒'.format(passed_time))
    return passed_time


def read_default_configuration():
    """
    查询默认参数
    1、传感器无效时间60s
    2、滑动窗口时间5s
    3、工作模式:09  01上报网关
    4、上报网关模式，有无人定频默认0s，默认关闭，步长上报默认1，默认开启
    5、上报网关模式，光照度定频0s，默认关闭，步长上报默认20 lux，默认开启
    6、传感器补偿参数   默认11%
    7、开关灯阈值   开灯:40,关灯60
    8、控制目标地址：空  数据域为 00 01 FF FF FF FF 00
    """
    engine.send_did('READ', '传感器无效时间D702', '')
    engine.expect_did('READ', '传感器无效时间D702', 无效时间=60)
    engine.send_did('READ', '上报间隔设置D004', '09')
    engine.expect_did('READ', '上报间隔设置D004', '09 05 00')
    engine.send_did('READ', '主动上报使能标志D005', '')
    engine.expect_did('READ', '主动上报使能标志D005', '09 01')
    engine.send_did('READ', '上报步长D103', '09')
    engine.expect_did('READ', '上报步长D103', '09 01')
    engine.send_did('READ', '上报步长D103', '0B')
    engine.expect_did('READ', '上报步长D103', '0B 20 00')
    engine.send_did('READ', '上报频率D104', '09')
    engine.expect_did('READ', '上报频率D104', '09 00 00')
    engine.send_did('READ', '上报频率D104', '0B')
    engine.expect_did('READ', '上报频率D104', '0B 00 00')
    engine.send_did('READ', '传感器数据补偿百分比D106', '0B')
    engine.expect_did('READ', '传感器数据补偿百分比D106', '0B 11')
    engine.send_did('READ', '传感器直接操作设备阀值D003', '0B')
    engine.expect_did('READ', '传感器直接操作设备阀值D003', '0B 28 3C')
    engine.send_did('READ', '控制目的设备地址D006', '')
    engine.expect_did('READ', '控制目的设备地址D006', '00 01 FF FF FF FF 00')


def modify_default_configuration(modify=True, verify=True):
    """
    修改默认参数，使其与默认参数不一致
    """
    if modify:
        engine.add_doc_info('修改默认参数，使其与默认参数不一致')
        engine.send_did('WRITE', '传感器无效时间D702', 无效时间=180)
        engine.expect_did('WRITE', '传感器无效时间D702', 无效时间=180)
        engine.send_did('WRITE', '主动上报使能标志D005', 传感器类型='人体红外移动', 上报命令='报警模式')
        engine.expect_did('WRITE', '主动上报使能标志D005', 传感器类型='人体红外移动', 上报命令='报警模式')
        engine.send_did('WRITE', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=1800)
        engine.expect_did('WRITE', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=1800)
        for sensor_type in ['人体红外移动', '照度']:
            engine.send_did('WRITE', '上报频率D104', 传感器类型=sensor_type, 定频=300)
            engine.expect_did('WRITE', '上报频率D104', 传感器类型=sensor_type, 定频=300)
        engine.send_did('WRITE', '上报步长D103', 传感器类型='人体红外移动', 步长='00')
        engine.expect_did('WRITE', '上报步长D103', 传感器类型='人体红外移动', 步长='00')
        engine.send_did('WRITE', '上报步长D103', '0B 50 00')
        engine.expect_did('WRITE', '上报步长D103', '0B 50 00')
        engine.send_did('WRITE', '传感器数据补偿百分比D106', '0B 12')
        engine.expect_did('WRITE', '传感器数据补偿百分比D106', '0B 12')
        engine.send_did('WRITE', '传感器直接操作设备阀值D003', '0B 32 50')
        engine.expect_did('WRITE', '传感器直接操作设备阀值D003', '0B 32 50')
        engine.send_did('WRITE', '控制目的设备地址D006', '00 01 14 00 00 00 01')
        engine.expect_did('WRITE', '控制目的设备地址D006', '00 01 14 00 00 00 01')
    if verify:
        engine.add_doc_info('查询修改后的参数，进行验证测试')
        engine.send_did('READ', '传感器无效时间D702', '')
        engine.expect_did('READ', '传感器无效时间D702', 无效时间=180)
        engine.send_did('READ', '上报间隔设置D004', 传感器类型='人体红外移动')
        engine.expect_did('READ', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=1800)
        engine.send_did('READ', '主动上报使能标志D005', '')
        engine.expect_did('READ', '主动上报使能标志D005', '09 05')
        for sensor_type in ['人体红外移动', '照度']:
            engine.send_did('READ', '上报频率D104', 传感器类型=sensor_type)
            engine.expect_did('READ', '上报频率D104', 传感器类型=sensor_type, 定频=300)
        engine.send_did('READ', '上报步长D103', '09')
        engine.expect_did('READ', '上报步长D103', '09 00')
        engine.send_did('READ', '上报步长D103', '0B')
        engine.expect_did('READ', '上报步长D103', '0B 50 00')
        engine.send_did('READ', '传感器数据补偿百分比D106', '0B')
        engine.expect_did('READ', '传感器数据补偿百分比D106', '0B 12')
        engine.send_did('READ', '传感器直接操作设备阀值D003', '0B')
        engine.expect_did('READ', '传感器直接操作设备阀值D003', '0B 32 50')
        engine.send_did('READ', '控制目的设备地址D006', '')
        engine.expect_did('READ', '控制目的设备地址D006', '00 01 14 00 00 00 01')


def return_to_factory():
    """
    恢复出厂设置
    暂不支持调试指令自动测试FC00，通过逐条设置实现恢复出厂设置
    """
    # engine.add_doc_info("发送调试指令，所有的状态和配置参数恢复至出厂参数")
    # engine.report_check_enable_all(True)
    # clear_gw_info()
    # engine.wait(14, allowed_message=False)
    # engine.expect_multi_dids("REPORT",
    #                          "通断操作C012", '00',
    #                          "导致状态改变的控制设备AIDC01A", config["测试设备地址"], ack=True)
    # engine.report_check_enable_all(False)
    # engine.send_did("WRITE", "自动测试FC00", 密码=config["设备PWD000A"], 自动测试命令="清除系统所有信息")
    # engine.expect_did("WRITE", "自动测试FC00", 密码=config["设备PWD000A"], 自动测试命令="清除系统所有信息")
    # engine.wait(10, tips='预留10s时间供设备清除系统所有信息')
    engine.add_doc_info('暂不支持调试指令自动测试FC00，通过逐条设置实现恢复出厂设置')
    engine.add_doc_info('修改参数，使其与默认参数一致')
    engine.send_did('WRITE', '传感器无效时间D702', 无效时间=60)
    engine.expect_did('WRITE', '传感器无效时间D702', 无效时间=60)
    engine.send_did('WRITE', '主动上报使能标志D005', 传感器类型='人体红外移动', 上报命令='上报网关')
    engine.expect_did('WRITE', '主动上报使能标志D005', 传感器类型='人体红外移动', 上报命令='上报网关')
    engine.send_did('WRITE', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=5)
    engine.expect_did('WRITE', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=5)
    for sensor_type in ['人体红外移动', '照度']:
        engine.send_did('WRITE', '上报频率D104', 传感器类型=sensor_type, 定频=0)
        engine.expect_did('WRITE', '上报频率D104', 传感器类型=sensor_type, 定频=0)
    engine.send_did('WRITE', '上报步长D103', 传感器类型='人体红外移动', 步长='01')
    engine.expect_did('WRITE', '上报步长D103', 传感器类型='人体红外移动', 步长='01')
    engine.send_did('WRITE', '上报步长D103', '0B 20 00')
    engine.expect_did('WRITE', '上报步长D103', '0B 20 00')
    engine.send_did('WRITE', '传感器数据补偿百分比D106', '0B 11')
    engine.expect_did('WRITE', '传感器数据补偿百分比D106', '0B 11')
    engine.send_did('WRITE', '传感器直接操作设备阀值D003', '0B 28 3C')
    engine.expect_did('WRITE', '传感器直接操作设备阀值D003', '0B 28 3C')
    engine.send_did('WRITE', '控制目的设备地址D006', '00 01 FF FF FF FF 00')
    engine.expect_did('WRITE', '控制目的设备地址D006', '00 01 FF FF FF FF 00')


def report_gateway_expect(expect_value="00", wait_times=[15], ack=True, quit_net=False, wait_enable=True):
    """
    添加上报测试
    :param wait_times:等待时间列表,自定义
    :param expect_value:期望上报的参数
    :param ack:默认为True,应答上报信息；为False时不应答上报信息
    :param quit_net:退网参数，默认为False，不发送退网指令，为True时，发送退网指令
    :param wait_enable: 是否进行等待测试，默认为True，验证等待125s，均无其他报文发出。
    """
    set_gw_info()  # 设置网关PANID信息，模拟设备入网
    # 定义添加上报
    for i, wait_time in enumerate(wait_times):
        ack_action = False
        if i == (len(wait_times) - 1):
            ack_action = ack
        engine.wait((wait_time - 1), allowed_message=False)
        engine.expect_multi_dids("REPORT",
                                 "读传感器数据B701", '09 ' + expect_value,
                                 "读传感器数据B701", '0B ** **', ack=ack_action)
    if wait_enable:
        engine.wait(125, allowed_message=False)
    if quit_net:
        engine.send_did("WRITE", "退网通知060B", 退网设备=config["测试设备地址"])
        engine.wait(5,tips='保持测试间隔5s')


def report_power_on_expect(expect_value="00", wait_times=[60], ack=True, wait_enable=True, power_on=True):
    """
    上电上报测试
    :param expect_value: 期望上报的参数
    :param wait_times: 等待时间列表
    :param ack: 默认为True,应答上报信息；为False时不应答上报信息
    :param wait_enable: 是否进行等待测试，默认为True，验证等待125s，均无其他报文发出。
    :param power_on：默认为True，表示进行断电重启，为False时表示不进行断电重启
    """
    if power_on:
        passed_time = power_control()
        if passed_time < wait_times[0]:
            wait_times[0] = wait_times[0] - passed_time
        else:
            engine.add_fail_test('等待时间参数设置错误')

    for i, data in enumerate(wait_times):
        ack_action = False
        if i == (len(wait_times) - 1):
            ack_action = ack
        engine.wait((wait_times[i] - 1), allowed_message=False)
        engine.expect_multi_dids("REPORT",
                                 "读传感器数据B701", '09 ' + expect_value,
                                 "读传感器数据B701", '0B ** **', ack=ack_action)
    if wait_enable:
        engine.wait(125, allowed_message=False)
