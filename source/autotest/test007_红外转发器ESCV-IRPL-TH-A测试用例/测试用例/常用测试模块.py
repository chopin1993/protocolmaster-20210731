# encoding:utf-8
# 导入测试引擎
import engine
from autotest.公共用例.public常用测试模块 import *
import time

config = engine.get_config()


def read_write_test():
    """
    抄读版本及控制测试，用时为passed_time
    """
    start_time = time.time()
    engine.wait(1, tips='抄读版本及控制测试')
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"])
    engine.wait(0.5)
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="温度", 上报命令="上报网关")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="温度", 上报命令="上报网关")
    engine.wait(0.5)
    for value in ['03', '04']:
        engine.send_did('READ', '传感器数据B691', value)
        engine.expect_did('READ', '传感器数据B691', value + ' ** **')
    passed_time = time.time() - start_time
    engine.add_doc_info('抄读版本及控制测试，用时为{:.3f}秒'.format(passed_time))
    return passed_time


def read_default_configuration():
    """
    查询默认参数
    1、默认工作模式为只上报网关01
    2、默认温湿度补偿参数为94 00 默认温度补偿-2摄氏度，湿度补偿0
    3、默认的心跳时间为1E 默认心跳时间为30min
    4、默认的红外补偿参数为2D 80 默认红外补偿时间为-45us
    """
    engine.send_did('READ', '主动上报使能标志D005', '')
    engine.expect_did('READ', '主动上报使能标志D005', '03 01')
    engine.send_did('READ', '心跳时间D101', '')
    engine.expect_did('READ', '心跳时间D101', '1E')
    engine.send_did('READ', '温湿度补偿参数FF08', '')
    engine.expect_did('READ', '温湿度补偿参数FF08', '94 00')
    engine.send_did('READ', '传感器数据补偿D107', '1F')
    engine.expect_did('READ', '传感器数据补偿D107', '1F 2D 80')


def modify_default_configuration(modify=True, verify=True):
    """
    修改默认参数，使其与默认参数不一致
    """
    if modify:
        engine.add_doc_info('修改参数，使其与默认参数不一致')
        engine.send_did('WRITE', '主动上报使能标志D005', '03 00')
        engine.expect_did('WRITE', '主动上报使能标志D005', '03 00')
        engine.send_did('WRITE', '心跳时间D101', '20')
        engine.expect_did('WRITE', '心跳时间D101', '20')
        engine.send_did('WRITE', '温湿度补偿参数FF08', '14 10')
        engine.expect_did('WRITE', '温湿度补偿参数FF08', '14 10')
        engine.send_did('WRITE', '传感器数据补偿D107', '1F 10 00')
        engine.expect_did('WRITE', '传感器数据补偿D107', '1F 10 00')

    if verify:
        engine.add_doc_info('验证修改后的参数，确认修改成功')
        engine.send_did('READ', '主动上报使能标志D005', '')
        engine.expect_did('READ', '主动上报使能标志D005', '03 00')
        engine.send_did('READ', '心跳时间D101', '')
        engine.expect_did('READ', '心跳时间D101', '20')
        engine.send_did('READ', '温湿度补偿参数FF08', '')
        engine.expect_did('READ', '温湿度补偿参数FF08', '14 10')
        engine.send_did('READ', '传感器数据补偿D107', '1F')
        engine.expect_did('READ', '传感器数据补偿D107', '1F 10 00')


def return_to_factory():
    """
    恢复出厂设置
    暂不支持调试指令自动测试FC00，通过逐条设置实现恢复出厂设置
    """
    engine.add_doc_info("发送调试指令，所有的状态和配置参数恢复至出厂参数")
    # engine.send_did("WRITE", "自动测试FC00", 密码=config["设备PWD000A"], 自动测试命令="清除系统所有信息")
    # engine.expect_did("WRITE", "自动测试FC00", 密码=config["设备PWD000A"], 自动测试命令="清除系统所有信息")
    # engine.wait(10, tips='预留10s时间供设备清除系统所有信息')
    engine.add_doc_info('暂不支持调试指令自动测试FC00和复位等待时间CD00，通过逐条设置实现恢复出厂设置')
    # engine.add_doc_info('修改参数，使其与默认参数一致')
    # engine.send_did('WRITE', '复位等待时间CD00', '00')
    # engine.expect_did('WRITE', '复位等待时间CD00', '00')
    # engine.wait(5, tips='通过复位等待时间CD00恢复出厂，预留充足时间')

    engine.add_doc_info('修改参数，使其与默认参数一致')
    engine.send_did('WRITE', '主动上报使能标志D005', '03 01')
    engine.expect_did('WRITE', '主动上报使能标志D005', '03 01')
    engine.send_did('WRITE', '心跳时间D101', '1E')
    engine.expect_did('WRITE', '心跳时间D101', '1E')
    engine.send_did('WRITE', '温湿度补偿参数FF08', '94 00')
    engine.expect_did('WRITE', '温湿度补偿参数FF08', '94 00')
    engine.send_did('WRITE', '传感器数据补偿D107', '1F 2D 80')
    engine.expect_did('WRITE', '传感器数据补偿D107', '1F 2D 80')


def report_gateway_expect(quit_net=False, wait_enable=True):
    """
    添加上报测试
    :param quit_net:退网参数，默认为False，不发送退网指令，为True时，发送退网指令
    :param wait_enable:等待验证参数，默认为True，表示等待验证25s,无报文上报，为False时表示不进行等待验证；
    """
    set_gw_info()  # 设置网关PANID信息，模拟设备入网
    engine.wait((15 - 1), allowed_message=False)
    engine.expect_did("NOTIFY", "传感器数据B691", '03 ** ** 04 ** **')
    if wait_enable:
        engine.wait(25, allowed_message=False)
    if quit_net:
        engine.send_did("WRITE", "退网通知060B", 退网设备=config["测试设备地址"])


def report_broadcast_expect(write_value="00 00 1F 10", scene_type="组地址按位组合"):
    """
    :param write_value:写入值
    :param scene_type:场景类型
    """

    if scene_type == "组地址按位组合":
        engine.broadcast_send_multi_dids("WRITE", [7, 8, 9, 10, 11], "BIT1", "红外直接发送0902", write_value)
    elif scene_type == "组地址按单字节组合":
        engine.broadcast_send_multi_dids("WRITE", [7, 8, 9, 10, 11], "U8", "红外直接发送0902", write_value)
    elif scene_type == "组地址按双字节组合":
        engine.broadcast_send_multi_dids("WRITE", [7, 8, 9, 10, 11], "U16", "红外直接发送0902", write_value)
    elif scene_type == "存在多个组地址的情况，组地址在前":
        engine.broadcast_send_multi_dids("WRITE",
                                         [7, 8, 9, 10, 11], "U8", "红外直接发送0902", write_value,
                                         [12, 13, 14, 15, 16], "U8", "通断操作C012", "82",
                                         [12, 13, 14, 15, 16], "U8", "通断操作C012", "84")
    elif scene_type == "存在多个组地址的情况，组地址在后":
        engine.broadcast_send_multi_dids("WRITE",
                                         [12, 13, 14, 15, 16], "U8", "通断操作C012", "02",
                                         [12, 13, 14, 15, 16], "U8", "通断操作C012", "04",
                                         [7, 8, 9, 10, 11], "U8", "红外直接发送0902", write_value)
    elif scene_type == "不同组地址混合 按单字节+按双字节+按位组合":
        engine.broadcast_send_multi_dids("WRITE",
                                         [7, 8, 9, 10, 11], "BIT1", "红外直接发送0902", write_value,
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
                                          180, 181, 182, 183, 184, 185, 186, 187, 188], "U16", "红外直接发送0902",
                                         write_value)
    elif scene_type == "测试同时控制6个虚拟设备":
        engine.broadcast_send_multi_dids("WRITE",
                                         [12, 13, 14, 15, 16], "U8", "通断操作C012", "81",
                                         [12, 13, 14, 15, 16], "U16", "通断操作C012", "82",
                                         [7, 8, 9, 10, 11], "BIT1", "红外直接发送0902", write_value,
                                         [7, 8, 9, 10, 11], "BIT1", "红外直接发送0902", "00 00 05 02",
                                         [7, 8, 9, 10, 11], "BIT1", "红外直接发送0902", "00 00 02 01",
                                         [7, 8, 9, 10, 11], "BIT1", "红外直接发送0902", "00 00 01 01",
                                         [7, 8, 9, 10, 11], "BIT1", "红外直接发送0902", "00 00 58 1B",
                                         [7, 8, 9, 10, 11], "BIT1", "红外直接发送0902", "00 00 01 04")
    elif scene_type == "sid大于255，组地址按位组合":
        engine.broadcast_send_multi_dids("WRITE", [220, 230, 250, 280, 289, 290, 291], "BIT1", "红外直接发送0902",
                                         write_value)
    elif scene_type == "sid大于255，组地址按双字节组合":
        engine.broadcast_send_multi_dids("WRITE", [220, 230, 250, 280, 289, 290, 291], "U16", "红外直接发送0902",
                                         write_value)
    elif scene_type == "面板配置情景模式组地址按位组合":
        # 配置面板信息
        panel01 = engine.create_role('触摸面板', 21)
        panel01.send_did("WRITE", "红外直接发送0902", write_value, gids=[7, 8, 9, 10, 11], gid_type="BIT1", taid=0xFFFFFFFF)
    elif scene_type == "面板配置情景模式组地址按单字节组合":
        # 配置面板信息
        panel01 = engine.create_role('触摸面板', 21)
        panel01.send_did("WRITE", "红外直接发送0902", write_value, gids=[7, 8, 9, 10, 11], gid_type="U8", taid=0xFFFFFFFF)
    elif scene_type == "面板配置情景模式组地址按双字节组合":
        # 配置面板信息
        panel01 = engine.create_role('触摸面板', 21)
        panel01.send_did("WRITE", "红外直接发送0902", write_value, gids=[7, 8, 9, 10, 11], gid_type="U16", taid=0xFFFFFFFF)
    else:
        engine.add_doc_info("不再既定场景测试范围内，请重试")

    engine.wait(10, allowed_message=False, tips="本次广播报文测试结束")
