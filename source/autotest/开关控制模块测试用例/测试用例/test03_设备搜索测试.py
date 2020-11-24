# encoding:utf-8
# 导入测试引擎
import engine
from .常用测试模块 import *

测试组说明 = "设备搜索测试"

config = engine.get_config()


def power_off_test():
    """
    前置工装通断电
    抄控器通过报文控制大功率计量遥控开关通断，实现给测试设备的通断电
    """
    # pane1 = engine.create_role("通断测试设备", 778856) # 创建陪测设备
    engine.send_did("WRITE", "通断操作C012", "01", dst=778856)
    engine.wait(seconds=5)
    engine.send_did("WRITE", "通断操作C012", "81", dst=778856)
    engine.wait(seconds=10)


def device_search0008(search_time, search_type):
    """
    APP设备搜索0008 定义函数
    """
    import time
    from tools.converter import hexstr2bytes
    start_time = time.time()
    passed = 0

    def cal_time(data):
        nonlocal passed, start_time
        passed = time.time() - start_time
        if data == hexstr2bytes(config["SN0007"]):
            return True
        else:
            return False

    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=search_time, 设备类型=search_type, dst=0xFFFFFFFF)
    engine.expect_multi_dids("SEARCH",
                             "SN0007", cal_time,
                             "DKEY0005", config["DKEY0005"],
                             "设备PWD000A", config["设备PWD000A"],
                             "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"],
                             timeout=search_time)

    engine.add_doc_info("search time {0}".format(passed))
    engine.wait(seconds=10, expect_no_message=True)


def test_APP设备搜索对设备类型的测试():
    """
    设备搜索类型测试
    1、测试搜索设备类型为全部类型 "FF FF FF FF"的时候，正常回复；
    2、测试搜索设备类型为开关控制模块类型 "31 71 10 10"的时候，正常回复；
    3、测试搜索设备类型为其他设备的类型 例如"31 71 20 01"的时候，不支持，不能回复；
    """

    engine.add_doc_info("测试开关控制模块针对设备搜索类型的响应情况：")
    # 针对支持的设备类型，可以正常回复；
    device_search0008(search_time=10, search_type="FF FF FF FF")
    device_search0008(search_time=10, search_type="31 71 10 10")
    # 针对不支持的设备类型，开关控制模块不回复；
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=10, 设备类型="31 71 20 20", dst=0xFFFFFFFF)
    engine.wait(seconds=10, expect_no_message=True)
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=10, 设备类型="31 71 20 01", dst=0xFFFFFFFF)
    engine.wait(seconds=10, expect_no_message=True)
    # 再次针对支持的设备类型，可以正常回复；
    device_search0008(search_time=10, search_type="FF FF FF FF")
    device_search0008(search_time=10, search_type="31 71 10 10")


def test_APP设备搜索对设备搜索时间的测试():
    """
    设备搜索时间测试
    1、针对设备搜索时间为30s时，连续运行3次，每次的报文回复时间不一致，则测试合格
    2、针对设备搜索时间为60s时，连续运行3次，每次的报文回复时间不一致，则测试合格
    3、针对设备搜索时间为300s时，连续运行3次，每次的报文回复时间不一致，则测试合格
    :return:
    """
    engine.add_doc_info("测试开关控制模块针对设备搜索时间的响应情况： 要求结果是随机上报")
    for i in range(3):
        device_search0008(search_time=30, search_type="31 71 10 10")

    # for i in range(3):
    #     device_search0008(search_time=60, search_type="31 71 10 10")
    #
    # for i in range(3):
    #     device_search0008(search_time=300, search_type="31 71 10 10")


def test_APP设备搜索对设备重发搜索的测试():
    """
    重发搜索测试
    """
    engine.add_doc_info("重发搜索测试，先将设备搜索时间为300s，等待30s后，再将设备搜索时间为10s，测试10s內可以正常回复：")
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=300, 设备类型="31 71 10 10", dst=0xFFFFFFFF)
    engine.wait(seconds=30, expect_no_message=True)
    device_search0008(search_time=10, search_type="31 71 10 10")


def test_APP设备搜索对设备断电重启的测试():
    """
    设备搜索断电测试
    前置大功率开关断电10s后重启
    """
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=30, 设备类型="31 71 10 10", dst=0xFFFFFFFF)
    # 前置大功率开关断电10s后重启
    engine.wait(seconds=30, expect_no_message=True)
    device_search0008(search_time=10, search_type="31 71 10 10")


def test_APP设备搜索对最大最小时间的测试():
    """
    最大最小时间验证
    """
    # 针对最小时间的测试
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=0, 设备类型="31 71 10 10", dst=0xFFFFFFFF)
    engine.expect_multi_dids("SEARCH",
                             "SN0007", config["SN0007"],
                             "DKEY0005", config["DKEY0005"],
                             "设备PWD000A", config["设备PWD000A"],
                             "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"],
                             timeout=10)
    # 针对最大时间的测试
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=0xFFFF, 设备类型="31 71 10 10", dst=0xFFFFFFFF)
    engine.wait(seconds=300, expect_no_message=True)
    device_search0008(search_time=10, search_type="31 71 10 10")


def test_APP设备指示0009():
    """
    APP设备指示0009
    """
    engine.send_did("WRITE", "APP设备指示0009")
    engine.expect_did("WRITE", "APP设备指示0009")
    engine.wait(seconds=10, expect_no_message=True)


def test_APP设备指示0009():
    """
    APP设备指示0009
    发送指示命令，验证设备的响应动作是否与要求一致。
    设备指示具体指示动作为第一路继电器翻转，1s变换一次状态，持续6s，设备指示过程中不允许载波通信，本地按键无效。
    """
    engine.send_did("WRITE", "APP设备指示0009")
    engine.expect_did("WRITE", "APP设备指示0009")
    engine.wait(seconds=10, expect_no_message=True)

    # 设备指示过程中抄读测试,不回复
    engine.send_did("WRITE", "APP设备指示0009")
    engine.expect_did("WRITE", "APP设备指示0009", "")

    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.wait(seconds=2, expect_no_message=True)
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.wait(seconds=2, expect_no_message=True)
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.wait(seconds=2, expect_no_message=True)

    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"])

    # 设备展示过程中断电重启
    engine.send_did("READ", "APP设备指示0009")
    engine.expect_did("READ", "APP设备指示0009")
    engine.wait(seconds=1, expect_no_message=True)

    # 控制大功率开关通断电，测试断电指示的过程中断电重启，开关控制模块仍可以正常运行
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"])


def test_静默时间000B():
    """
    静默时间000B
    验证在静默时间内，是否可以不响应搜索报文
    1、首先验证设备搜索功能正常
    2、设置静默时间
    3、静默时间内多次进行设备搜索，均不回复
    4、静默时间结束，可以正常响应设备搜索
    """
    device_search0008(search_time=10, search_type="31 71 10 10")
    engine.send_did("WRITE", "静默时间000B", 静默时间=60)
    engine.expect_did("WRITE", "静默时间000B", 静默时间=60)

    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=10, 设备类型="31 71 10 10", dst=0xFFFFFFFF)
    engine.wait(seconds=10, expect_no_message=True)
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=10, 设备类型="31 71 10 10", dst=0xFFFFFFFF)
    engine.wait(seconds=10, expect_no_message=True)
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=40, 设备类型="31 71 10 10", dst=0xFFFFFFFF)
    engine.wait(seconds=40, expect_no_message=True)

    device_search0008(search_time=10, search_type="31 71 10 10")

    # 静默时间内的断电重启测试
    engine.add_doc_info("静默时间内的断电重启测试")
    device_search0008(search_time=10, search_type="31 71 10 10")
    engine.send_did("WRITE", "静默时间000B", 静默时间=60)
    engine.expect_did("WRITE", "静默时间000B", 静默时间=60)
    power_off_test()  # 通过前置测试工装通断电，用时15s
    device_search0008(search_time=10, search_type="31 71 10 10")

    # 静默时间的最大值、最小值测试

    engine.add_doc_info("静默时间的最小值测试")
    device_search0008(search_time=10, search_type="31 71 10 10")
    engine.send_did("WRITE", "静默时间000B", 静默时间=0)
    engine.expect_did("WRITE", "静默时间000B", 静默时间=0)
    device_search0008(search_time=10, search_type="31 71 10 10")
    engine.add_doc_info("静默时间的最大值测试")
    device_search0008(search_time=10, search_type="31 71 10 10")

    engine.send_did("WRITE", "静默时间000B", 静默时间=65535)
    engine.expect_did("WRITE", "静默时间000B", 静默时间=65535)
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=10, 设备类型="31 71 10 10", dst=0xFFFFFFFF)
    engine.wait(seconds=10, expect_no_message=True)
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=60, 设备类型="31 71 10 10", dst=0xFFFFFFFF)
    engine.wait(seconds=60, expect_no_message=True)
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=300, 设备类型="31 71 10 10", dst=0xFFFFFFFF)
    engine.wait(seconds=300, expect_no_message=True)

    engine.add_doc_info("静默时间的重新设置为60s测试")
    engine.send_did("WRITE", "静默时间000B", 静默时间=60)
    engine.expect_did("WRITE", "静默时间000B", 静默时间=60)
    engine.wait(60, expect_no_message=True)
    device_search0008(search_time=10, search_type="31 71 10 10")

    # 入网后不再支持设备搜索报文测试


def test_设备入网后不再支持设备搜索():
    """
    设备入网后不再支持设备搜索测试
    1、首先验证刚烧写完成的设备，设备搜索正常；
    2、测试设备加入网关后，设备不再响应设备搜索
    3、测试设备清除PANID后，设备再次响应设备搜索
    """
    engine.add_doc_info("1、首先验证刚烧写完成的设备，设备搜索正常；")
    device_search0008(search_time=10, search_type="31 71 10 10")

    engine.add_doc_info("2、测试设备加入网关后，设备不再响应设备搜索")
    set_gw_info() # 设置网关PANID信息，模拟设备入网
    engine.wait(20)
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=10, 设备类型="31 71 10 10", dst=0xFFFFFFFF)
    engine.wait(seconds=10, expect_no_message=True)

    engine.add_doc_info("3、测试设备清除PANID后，设备再次响应设备搜索")
    clear_gw_info() #清除网关PANID信息，模拟出厂设备
    engine.wait(20)
    device_search0008(search_time=10, search_type="31 71 10 10")