# encoding:utf-8
# 导入测试引擎
import engine
from .常用测试模块 import *

测试组说明 = "状态同步测试"
"""
红外转发器的状态同步测试，较执行器类，功能较少，更加简单。
"""
config = engine.get_config()


def test_添加上报():
    """
    01_添加上报测试
    1、设备收到网关发送的注册帧后等15s（允许1s误差）以后开始上报；
    2、添加上报的上报方式为00不可靠上报，所以没有10s、100s重试上报测试机制，此处不需测试；
    """
    engine.report_check_enable_all(True)  # 打开上报检测
    engine.add_doc_info("1、设备收到网关发送的注册帧后等15s（允许1s误差）以后开始上报")
    engine.add_doc_info('（1）测试sid > 100的情况，sid = 280的情况下，测试网关正常应答的情况')
    set_gw_info(panid=1100, sid=280)
    engine.wait(15 - 1, allowed_message=False)
    engine.expect_did("NOTIFY", "传感器数据B691", '03 ** ** 04 ** **')
    engine.wait(25, allowed_message=False)
    engine.send_did("WRITE", "退网通知060B", 退网设备=config["测试设备地址"])

    engine.add_doc_info('（2）测试sid < 100的情况，sid = 8的情况下，测试网关正常应答的情况')
    report_gateway_expect()

    engine.add_doc_info("2、添加上报的上报方式为00不可靠上报，所以没有10s、100s重试上报测试机制，此处不需测试；")
    engine.report_check_enable_all(False)  # 关闭上报检测


def test_上电上报():
    """
    02_上电上报测试
    红外转发器不支持上电上报，该项暂不测试；
    """
    engine.report_check_enable_all(True)  # 打开上报检测
    engine.add_doc_info("1、红外转发器不支持上电上报，该项暂不测试；")
    engine.report_check_enable_all(False)  # 关闭上报检测


def test_工作模式测试():
    """
    03_工作模式测试
    1、默认工作模式为只上报网关，测试此种情况下，步长上报和心跳上报的上报情况（上报正常）；
    2、修改工作模式为不上报，测试此种情况下，步长上报和心跳上报的上报情景（均不上报）；
    3、将参数修改回默认参数，继续其他测试项目；
    """
    engine.report_check_enable_all(True)  # 打开上报检测
    engine.add_doc_info('默认情况下，工作模式为只上报网关，步长为默认不可修改，心跳时间为30min，为便于测试，将心跳时间修改为1min')
    engine.send_did('READ', '主动上报使能标志D005', '')
    engine.expect_did('READ', '主动上报使能标志D005', '03 01')
    engine.send_did('READ', '心跳时间D101', '')
    engine.expect_did('READ', '心跳时间D101', '1E')
    engine.send_did('WRITE', '心跳时间D101', '01')
    engine.expect_did('WRITE', '心跳时间D101', '01')

    engine.add_doc_info("1、默认工作模式为只上报网关，测试此种情况下，步长上报和心跳上报的上报情况（上报正常）；")
    engine.add_doc_info('（1）步长上报，温度每变化1°C，湿度变化4%，主动上报网关，上报步长写为定值，不支持读取和设置。'
                        '因为本设备不支持SWB协议，无法人工设置传感器数据，所以需要人工补测，进行相关的验证')

    engine.add_doc_info('（2）心跳上报，连续监控一段时间，测试3次心跳上报正常，本次测试将心跳设置为1min')
    for heartbeat_time in [1]:
        for i in range(3):
            engine.add_doc_info('心跳时间为{}min时，第{}轮上报测试'.format(heartbeat_time, i + 1))
            if i == 0:
                engine.expect_did("NOTIFY", "传感器数据B691", '03 ** ** 04 ** **', timeout=heartbeat_time * 60 + 1)
                continue
            engine.wait(heartbeat_time * 60 - 1, allowed_message=False, tips='两次心跳上报间隔，要求无多余报文')
            engine.expect_did("NOTIFY", "传感器数据B691", '03 ** ** 04 ** **')

    engine.add_doc_info('2、修改工作模式为不上报，测试此种情况下，步长上报和心跳上报的上报情景（均不上报）；')
    engine.send_did('WRITE', '主动上报使能标志D005', '03 00')
    engine.expect_did('WRITE', '主动上报使能标志D005', '03 00')

    engine.add_doc_info('步长上报，工作模式为不上报的时候，不再上报。'
                        '因为本设备不支持SWB协议，无法人工设置传感器数据，所以需要人工补测，进行相关的验证')

    engine.add_doc_info('心跳上报，本次测试将心跳设置为1min，连续监控3min以上，要求无心跳上报数据')
    engine.wait(200, allowed_message=False, tips='连续监控3min以上，要求无心跳上报数据')

    engine.add_doc_info('3、将参数修改回默认参数，继续其他测试项目；')
    engine.send_did('WRITE', '主动上报使能标志D005', '03 01')
    engine.expect_did('WRITE', '主动上报使能标志D005', '03 01')
    engine.send_did('WRITE', '心跳时间D101', '1E')
    engine.expect_did('WRITE', '心跳时间D101', '1E')
    engine.report_check_enable_all(False)  # 关闭上报检测


def test_步长上报():
    """
    04_步长上报
    温度每变化1°C，湿度变化4%，主动上报网关，上报步长写为定值，不支持读取和设置。
    1、测试温度上升或者下降1℃以上，湿度基本不变，测试2种情况，步长上报正常；
    2、测试湿度上升或者下降4%以上，温度基本不变，测试2种情况，步长上报正常；
    3、测试温度和湿度，都在变化值之上，测试步长上报正常；
    4、测试步长上报的过程中，发生心跳上报干扰，心跳上报不会影响步长上报的基准值；
    """
    engine.report_check_enable_all(True)  # 打开上报检测
    engine.add_doc_info('步长上报，温度每变化1°C，湿度变化4%，主动上报网关，上报步长写为定值，不支持读取和设置。'
                        '因为本设备不支持SWB协议，无法人工设置传感器数据，所以需要人工补测，进行相关的验证')
    engine.report_check_enable_all(False)  # 关闭上报检测


def test_心跳上报():
    """
    05_心跳上报
    1、将红外转发器安装在稳定的环境中，去除步长上报的干扰，然后测试不同的情况下，测试心跳上报正常；
    2、测试心跳上报的过程中，发生步长上报干扰，步长上报不会影响心跳上报的间隔时间；
    3、将参数修改回默认参数，继续其他测试项目；
    """
    engine.report_check_enable_all(True)  # 打开上报检测
    engine.add_doc_info('1、将红外转发器安装在稳定的环境中，去除步长上报的干扰，然后测试不同的情况下，测试心跳上报正常；')

    engine.add_doc_info('分别测试，心跳时间为2min、0min、5min时，(心跳时间为1min上述已测试，所以此处测试2min)'
                        '心跳时间不为0时，连续监控3次心跳以上，均可以正常上报，'
                        '心跳时间为0时，连续监控5min以上，要求无上报')

    for heartbeat_time in [2, 0, 5]:
        engine.send_did('WRITE', '心跳时间D101', 心跳时间=heartbeat_time)
        engine.expect_did('WRITE', '心跳时间D101', 心跳时间=heartbeat_time)
        engine.send_did('READ', '心跳时间D101', '')
        engine.expect_did('READ', '心跳时间D101', 心跳时间=heartbeat_time)
        engine.wait(2, '预留2s测试间隔')

        if heartbeat_time == 0:
            engine.add_doc_info('心跳时间为0时，连续监控5min以上，要求无上报，说明心跳正常')
            engine.wait(320, allowed_message=False, tips='连续监控5min以上，要求无上报')
            continue

        for i in range(3):
            engine.add_doc_info('心跳时间为{}min时，第{}轮上报测试'.format(heartbeat_time, i + 1))
            if i == 0:
                engine.add_doc_info('设置不同心跳时间后，第一次上报的时间不可控，'
                                    '所以第一次等待时间为心跳时间*60+1，其后测试严格按照心跳时间验证')
                engine.expect_did("NOTIFY", "传感器数据B691", '03 ** ** 04 ** **', timeout=heartbeat_time * 60 + 1)
                continue
            engine.wait(heartbeat_time * 60 - 1, allowed_message=False, tips='两次心跳上报间隔，要求无多余报文')
            engine.expect_did("NOTIFY", "传感器数据B691", '03 ** ** 04 ** **')

    engine.add_doc_info('2、测试心跳上报的过程中，发生步长上报干扰，步长上报不会影响心跳上报的间隔时间；'
                        '因为本设备不支持SWB协议，无法人工设置传感器数据，所以需要人工补测，进行相关的验证')

    engine.add_doc_info('3、将参数修改回默认参数，继续其他测试项目；')
    engine.send_did('WRITE', '心跳时间D101', 心跳时间=30)
    engine.expect_did('WRITE', '心跳时间D101', 心跳时间=30)
    engine.send_did('READ', '心跳时间D101', '')
    engine.expect_did('READ', '心跳时间D101', 心跳时间=30)
    engine.report_check_enable_all(False)  # 关闭上报检测


def test_广播报文控制测试():
    """
    06_广播报文控制测试
    因为红外转发器控制红外设备，控制结果无回复，所以此处测试需要结合人工测试进行验证，或者后期增加其他检测方式；
    本项测试前，需要添加前置条件，提前学习6个虚拟设备的红外按钮；
    1、组地址按位组合
    2、组地址按单字节组合
    3、组地址按双字节组合
    4、存在多个组地址的情况，组地址在前
    5、存在多个组地址的情况，组地址在后
    6、不同组地址混合 按单字节+按双字节+按位组合
    7、模拟220字节超长情景模式报文测试
    8、测试同时控制6个虚拟设备(目前手机端最多支持6个虚拟设备)
    9、验证sid大于255的情况，sid=280情况下，按位、按双字节情景模式模式控制
    10、设置回常用的网关和PANID
    11、面板配置情景模式，分别组地址按位组合、按单字节组合、按双字节组合
    """
    engine.report_check_enable_all(True)  # 打开上报检测

    engine.add_doc_info("1、组地址按位组合")
    report_broadcast_expect(scene_type='组地址按位组合')

    engine.add_doc_info("2、组地址按单字节组合")
    report_broadcast_expect(scene_type='组地址按单字节组合')

    engine.add_doc_info("3、组地址按双字节组合")
    report_broadcast_expect(scene_type='组地址按双字节组合')

    engine.add_doc_info("4、存在多个组地址的情况，组地址在前")
    report_broadcast_expect(scene_type='存在多个组地址的情况，组地址在前')

    engine.add_doc_info("5、存在多个组地址的情况，组地址在后")
    report_broadcast_expect(scene_type='存在多个组地址的情况，组地址在后')

    engine.add_doc_info("6、不同组地址混合 按单字节+按双字节+按位组合")
    report_broadcast_expect(scene_type='不同组地址混合 按单字节+按双字节+按位组合')

    engine.add_doc_info("7、模拟220字节超长情景模式报文测试")
    # 网关发送情景模式报文，最长为220个字节，使报文长度接近220个字节，下列为219个字节
    report_broadcast_expect(scene_type='模拟220字节超长情景模式报文测试')

    engine.add_doc_info("8、测试同时控制6个虚拟设备")
    # 本项测试前，需要将家庭APP支持的6个虚拟设备，全部学习开关状态
    report_broadcast_expect(scene_type='测试同时控制6个虚拟设备')

    engine.add_doc_info("9、验证sid大于255的情况，sid=280情况下，按位、按双字节情景模式模式控制")
    engine.add_doc_info('sid大于255时，超出单字节范围，单字节无法表示，所以不需要验证按单字节情景模式控制')
    set_gw_info(panid=1100, sid=280)
    engine.wait(15 - 1, allowed_message=False)
    engine.expect_did("NOTIFY", "传感器数据B691", '03 ** ** 04 ** **')
    engine.wait(25, allowed_message=False)

    engine.add_doc_info('sid大于255，组地址按位组合')
    report_broadcast_expect(scene_type='sid大于255，组地址按位组合')

    engine.add_doc_info('sid大于255，组地址按双字节组合')
    report_broadcast_expect(scene_type='sid大于255，组地址按双字节组合')

    engine.add_doc_info('10、设置回常用的网关信息和PANID')
    report_gateway_expect()

    engine.add_doc_info('11、面板配置情景模式，分别组地址按位组合、按单字节组合、按双字节组合')

    engine.add_doc_info('面板配置情景模式组地址按位组合')
    report_broadcast_expect(scene_type='面板配置情景模式组地址按位组合')

    engine.add_doc_info('面板配置情景模式组地址按单字节组合')
    report_broadcast_expect(scene_type='面板配置情景模式组地址按单字节组合')

    engine.add_doc_info('面板配置情景模式组地址按双字节组合')
    report_broadcast_expect(scene_type='面板配置情景模式组地址按双字节组合')
    engine.report_check_enable_all(False)  # 关闭上报检测
