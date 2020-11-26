# encoding:utf-8
# 导入测试引擎
import engine
from .常用测试模块 import *

测试组说明 = "设备搜索测试"

config = engine.get_config()


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

    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=search_time,
                    设备类型=search_type, taid=0xFFFFFFFF, gids=[0], gid_type="U8")

    engine.expect_multi_dids("SEARCH",
                             "SN0007", cal_time,
                             "DKEY0005", config["DKEY0005"],
                             "设备PWD000A", config["设备PWD000A"],
                             "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"],
                             timeout=(search_time + 0.5))

    engine.add_doc_info("search time {0}".format(passed))
    engine.wait(10, allowed_message=False)


def test_APP设备搜索对设备类型的测试():
    """
    01_设备搜索类型测试
    1、测试搜索设备类型为全部类型 "FF FF FF FF"的时候，正常回复；
    2、测试搜索设备类型为开关控制模块类型 "31 71 10 10"的时候，正常回复；
    3、测试搜索设备类型为其他设备的类型 例如"31 71 20 01"的时候，不支持，不能回复；
    """

    engine.add_doc_info("测试开关控制模块针对设备搜索类型的响应情况：")
    # 针对支持的设备类型，可以正常回复；
    engine.add_doc_info("针对支持的设备类型，可以正常回复")
    device_search0008(search_time=10, search_type="FF FF FF FF")
    device_search0008(search_time=10, search_type="31 71 10 10")
    # 针对不支持的设备类型，开关控制模块不回复；
    engine.add_doc_info("针对不支持的设备类型，开关控制模块不回复")
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=10,
                    设备类型="31 71 20 20", taid=0xFFFFFFFF, gids=[0], gid_type="U8")
    engine.wait(11, allowed_message=False)
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=10,
                    设备类型="31 71 20 01", taid=0xFFFFFFFF, gids=[0], gid_type="U8")
    engine.wait(11, allowed_message=False)
    # 再次针对支持的设备类型，可以正常回复；
    engine.add_doc_info("针对支持的设备类型，可以正常回复")
    device_search0008(search_time=10, search_type="FF FF FF FF")
    device_search0008(search_time=10, search_type="31 71 10 10")


def test_APP设备搜索对设备搜索时间的测试():
    """
    02_设备搜索时间测试
    1、针对设备搜索时间为10s时，连续运行3次，每次的报文回复时间不一致，则测试合格
    2、针对设备搜索时间为60s时，连续运行3次，每次的报文回复时间不一致，则测试合格
    3、针对设备搜索时间为300s时，连续运行3次，每次的报文回复时间不一致，则测试合格
    :return:
    """
    engine.add_doc_info("测试开关控制模块针对设备搜索时间的响应情况： 要求结果是随机上报")
    for i in range(3):
        device_search0008(search_time=10, search_type="31 71 10 10")

    for i in range(3):
        device_search0008(search_time=60, search_type="31 71 10 10")

    # for i in range(3):
    #     device_search0008(search_time=300, search_type="31 71 10 10")


def test_APP设备搜索对设备重发搜索的测试():
    """
    03_重发设备搜索测试
    1、首先发送搜索时间为300s的设备搜索
    2、等待30s，如果此时没有报文上报，则再次下发搜索时间为10s的设备搜索，开关控制模块回复正常
    """
    engine.add_doc_info("重发搜索测试，先将设备搜索时间为300s，等待30s后，再将设备搜索时间为10s，测试10s內可以正常回复：")
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=300,
                    设备类型="31 71 10 10", taid=0xFFFFFFFF, gids=[0], gid_type="U8")
    engine.wait(30, allowed_message=False)
    device_search0008(search_time=10, search_type="31 71 10 10")


def test_APP设备搜索对设备断电重启的测试():
    """
    04_设备搜索中断电测试
    1、测试设备搜索时间=10s，设备搜索正常
    2、测试设备搜索时间=60s，然后通过前置工装断电重启，等待60s无上报
    3、再次测试设备搜索时间=10s，设备搜索正常
    """
    device_search0008(search_time=10, search_type="31 71 10 10")

    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=60,
                    设备类型="31 71 10 10", taid=0xFFFFFFFF, gids=[0], gid_type="U8")

    engine.add_doc_info("前置工装断电重启")
    power_off_test()
    engine.add_doc_info("断电重启后，要求设备无上报信息，则说明断电后设备搜索流程中止")
    engine.wait(60, allowed_message=False)

    device_search0008(search_time=10, search_type="31 71 10 10")


def test_APP设备搜索最大最小时间的测试():
    """
    05_设备搜索最大最小时间测试
    1、测试设备搜索时间=10s，设备搜索正常
    2、测试最小时间0秒，实际开关控制模块按照设备搜索时间=10s进行处理
    3、测试最大时间65535秒= 0xFFFF，等待300s后，开关控制模块仍未上报，再次触发10s的设备搜索，开关控制模块回复正常
    """
    engine.add_doc_info("测试设备搜索时间=10s，设备搜索正常")
    device_search0008(search_time=10, search_type="31 71 10 10")

    engine.add_doc_info("针对设备搜索最小时间的测试")
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=0,
                    设备类型="31 71 10 10", taid=0xFFFFFFFF, gids=[0], gid_type="U8")
    engine.expect_multi_dids("SEARCH",
                             "SN0007", config["SN0007"],
                             "DKEY0005", config["DKEY0005"],
                             "设备PWD000A", config["设备PWD000A"],
                             "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"],
                             timeout=10 + 0.5)
    engine.wait(10, allowed_message=False)

    engine.add_doc_info("针对设备搜索最大时间的测试")
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=0xFFFF,
                    设备类型="31 71 10 10", taid=0xFFFFFFFF, gids=[0], gid_type="U8")
    engine.wait(300, allowed_message=False)
    engine.add_doc_info("连续300s无上报信息，再次触发10s的设备搜索报文，设备回复正常")
    device_search0008(search_time=10, search_type="31 71 10 10")


def test_APP设备指示0009():
    """
    06_APP设备指示0009
    1、发送指示命令，验证设备的响应动作是否与要求一致。
    设备指示具体指示动作为第一路继电器翻转，1s变换一次状态，持续6s，设备指示过程中不允许载波通信，本地按键无效。
    """
    engine.send_did("WRITE", "APP设备指示0009", "")
    engine.expect_did("WRITE", "APP设备指示0009", "")
    engine.wait(6, allowed_message=False)
    engine.wait(1)
    #  设备指示过程中进行抄读测试,设备指示过程中不允许载波通信验证
    engine.add_doc_info("设备指示过程中进行抄读测试,设备指示过程中不允许载波通信验证")
    engine.send_did("WRITE", "APP设备指示0009", "")
    engine.expect_did("WRITE", "APP设备指示0009", "")

    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.wait(2, allowed_message=False)
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.wait(2, allowed_message=False)
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.wait(2, allowed_message=False)
    engine.add_doc_info("设备指示结束后，可以正常进行载波通信验证")
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"])
    engine.wait(1)
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(1)
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")

def test_APP设备指示中断电测试():
    """
    07_APP设备指示中断电测试
    1、设备指示过程中被断电重启，开关控制模块退出设备指示，设备载波通信恢复正常
    """
    engine.add_doc_info("设备指示过程中断电重启，退出设备指示，设备载波通信恢复正常")
    engine.send_did("WRITE", "APP设备指示0009", "")
    engine.expect_did("WRITE", "APP设备指示0009", "")
    engine.add_doc_info("设备指示过程中进行抄读测试,设备指示过程中不允许载波通信验证")
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.wait(3, allowed_message=False)
    # 控制前置工装通断电，测试断电指示的过程中断电重启，开关控制模块仍可以正常运行
    engine.add_doc_info("控制前置工装通断电，测试断电指示的过程中断电重启，开关控制模块仍可以正常运行")
    power_off_test()
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"])

def test_静默时间000B():
    """
    08_静默时间000B
    验证在静默时间内，是否可以不响应搜索报文
    1、首先验证设备搜索功能正常
    2、设置静默时间60s
    3、静默时间内多次进行设备搜索，均不回复
    4、静默时间结束，可以正常响应设备搜索
    """
    device_search0008(search_time=10, search_type="31 71 10 10")
    engine.send_did("WRITE", "静默时间000B", 静默时间=60)
    engine.expect_did("WRITE", "静默时间000B", 静默时间=60)

    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=10,
                    设备类型="31 71 10 10", taid=0xFFFFFFFF, gids=[0], gid_type="U8")
    engine.wait(10, allowed_message=False)
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=10,
                    设备类型="31 71 10 10", taid=0xFFFFFFFF, gids=[0], gid_type="U8")
    engine.wait(10, allowed_message=False)
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=40,
                    设备类型="31 71 10 10", taid=0xFFFFFFFF, gids=[0], gid_type="U8")
    engine.wait(40, allowed_message=False)

    device_search0008(search_time=10, search_type="31 71 10 10")


def test_静默时间000B断电测试():
    """
    09_静默时间000B断电测试
    验证在静默时间内，是否可以不响应搜索报文
    1、首先验证设备搜索功能正常
    2、设置静默时间300s,测试静默时间内抄读版本及控制通断均正常
    3、静默时间内多次进行设备搜索，均不回复
    4、控制前置工装断电重启，再次测试设备搜索正常，说明断电后设备静默时间失效
    """
    device_search0008(search_time=10, search_type="31 71 10 10")

    engine.send_did("WRITE", "静默时间000B", 静默时间=300)
    engine.expect_did("WRITE", "静默时间000B", 静默时间=300)
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"])
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(1)
    engine.send_did("READ", "通断操作C012")
    engine.expect_did("READ", "通断操作C012", "00")
    # 进行多次设备搜索报文测试
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=10,
                    设备类型="31 71 10 10", taid=0xFFFFFFFF, gids=[0], gid_type="U8")
    engine.wait(10, allowed_message=False)
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=20,
                    设备类型="31 71 10 10", taid=0xFFFFFFFF, gids=[0], gid_type="U8")
    engine.wait(20, allowed_message=False)

    # 静默时间内的断电重启测试
    engine.add_doc_info("静默时间内的断电重启测试")
    power_off_test()  # 工装断电重启用时约20s，仍在300s静默时间范围内
    device_search0008(search_time=10, search_type="31 71 10 10")
    device_search0008(search_time=20, search_type="FF FF FF FF")


def test_静默时间最大值最小值测试():
    """
    10_静默时间最大值最小值测试
    1、首先验证设备搜索功能正常
    2、设置静默时间0s，然后立即触发设备搜索，发现可以正常搜索到开关控制模块；
    3、设置静默时间65535s，然后立即触发设备搜索，发现可以搜索不到开关控制模块；
    4、再等待300s后，再次触发设备搜索，发现可以搜索不到开关控制模块；
    5、重新设置静默时间为60s，等待静默时间失效，再次触发设备搜索，发现可以搜索到开关控制模块；
    """
    # 静默时间的最小值测试
    engine.add_doc_info("静默时间的最小值测试：设置静默时间0s，然后立即触发设备搜索，发现可以正常搜索到开关控制模块")
    device_search0008(search_time=10, search_type="31 71 10 10")
    engine.send_did("WRITE", "静默时间000B", 静默时间=0)
    engine.expect_did("WRITE", "静默时间000B", 静默时间=0)
    device_search0008(search_time=10, search_type="31 71 10 10")

    # 静默时间的最大值测试
    engine.add_doc_info("静默时间的最大值测试")
    device_search0008(search_time=10, search_type="31 71 10 10")
    engine.send_did("WRITE", "静默时间000B", 静默时间=65535)
    engine.expect_did("WRITE", "静默时间000B", 静默时间=65535)

    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=10,
                    设备类型="31 71 10 10", taid=0xFFFFFFFF, gids=[0], gid_type="U8")
    engine.wait(10, allowed_message=False)
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=60,
                    设备类型="31 71 10 10", taid=0xFFFFFFFF, gids=[0], gid_type="U8")
    engine.wait(60, allowed_message=False)
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=300,
                    设备类型="31 71 10 10", taid=0xFFFFFFFF, gids=[0], gid_type="U8")
    engine.wait(300, allowed_message=False)
    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=10,
                    设备类型="31 71 10 10", taid=0xFFFFFFFF, gids=[0], gid_type="U8")
    engine.wait(10, allowed_message=False)

    engine.add_doc_info("重新设置静默时间为60s，等待静默时间失效，再次触发设备搜索，发现可以搜索到开关控制模块")
    engine.send_did("WRITE", "静默时间000B", 静默时间=60)
    engine.expect_did("WRITE", "静默时间000B", 静默时间=60)
    engine.wait(60, allowed_message=False)

    device_search0008(search_time=10, search_type="31 71 10 10")


def test_设备入网后不再支持设备搜索():
    """
    11_设备入网后不再支持设备搜索测试
    1、首先验证刚烧写完成的设备，设备搜索正常；
    2、测试设备加入网关后，设备不再响应设备搜索
    3、测试设备清除PANID后，设备再次响应设备搜索
    """
    engine.add_doc_info("1、首先验证刚烧写完成的设备，设备搜索正常；")
    device_search0008(search_time=10, search_type="31 71 10 10")

    engine.add_doc_info("2、测试设备加入网关后，设备不再响应设备搜索")
    set_gw_info()  # 设置网关PANID信息，模拟设备入网
    # engine.expect_multi_dids("REPORT",
    #                          "通断操作C012", "00",
    #                          "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=16, ack=True)
    engine.wait(20)

    engine.send_did("SEARCH", "APP设备搜索0008", 搜索类型="未注册节点", 搜索时间=10,
                    设备类型="31 71 10 10", taid=0xFFFFFFFF, gids=[0], gid_type="U8")
    engine.wait((10+1), allowed_message=False)

    engine.add_doc_info("3、测试设备清除PANID后，设备再次响应设备搜索")
    clear_gw_info()  # 清除网关PANID信息，模拟出厂设备
    # engine.expect_multi_dids("REPORT",
    #                          "通断操作C012", "00",
    #                          "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=16, ack=True)
    engine.wait(20)
    device_search0008(search_time=10, search_type="31 71 10 10")
