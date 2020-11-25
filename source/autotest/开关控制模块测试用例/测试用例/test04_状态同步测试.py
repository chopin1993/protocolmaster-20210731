# encoding:utf-8
# 导入测试引擎
import engine
from .常用测试模块 import *

测试组说明 = "状态同步测试"
"""
参数说明	                    原时间参数（单位：s）|优化后时间参数（单位：100ms）
状态改变等待时间	                    5	       |        13
订阅者间间隔	                        1	       |        2
情景模式控制各设备上报间隔	            2          |  	    5
"""
config = engine.get_config()


def test_测试前环境搭建():
    """
    01_测试前环境搭建
    因为状态同步部分涉及到设备入网，抄控器会被设置网关PANID，
    所以也需要给测试工装设置同样的网关PANID，保证通信控制通断正常；
    """

    engine.send_local_msg("设置PANID", config["panid"])
    engine.expect_local_msg("确认")
    engine.send_did("WRITE", "载波芯片注册信息0603",
                    aid=778856,
                    panid=config["panid"],
                    pw=39751,
                    device_gid=config["抄控器默认源地址"],
                    sid=1,
                    taid=778856)
    engine.expect_did("WRITE", "载波芯片注册信息0603", "** ** ** ** ** **", said=778856)
    engine.wait(20)


def test_添加上报():
    """
    02_添加上报测试
    1、设备收到网关发送的注册帧后等15s（允许1s误差）以后开始上报
    2、设备添加上报后，收不到网关应答，进行10s、100s重试，重试结束则本次添加上报结束
    3、如果10s重试上报过程中，收到网关应答，不再进行100重试上报
    4、测试添加网关后，添加上报前，是否可以正常被控制通断
    5、测试添加上报重试的过程中，是否可以正常被控制通断
    6、继电器处于断开的状态上述已验证，再次测试继电器处于闭合的状态，进行添加上报测试；
    """
    engine.add_doc_info("1、设备收到网关发送的注册帧后等15s（允许1s误差）以后开始上报")
    set_gw_info()  # 设置网关PANID信息，模拟设备入网
    engine.wait(14.5, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "00",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=1, ack=True)
    # 测试入网结束，再次测试开关控制模块添加入网，需要发送退网通知060B
    engine.send_did("WRITE", "退网通知060B", 退网设备=config["测试设备地址"])

    engine.add_doc_info("2、设备添加上报后，收不到网关应答，进行10s、100s重试，重试结束则本次添加上报结束")
    set_gw_info()  # 设置网关PANID信息，模拟设备入网
    engine.wait(14.5, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "00",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=1)
    engine.wait(9.5, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "00",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=1)
    engine.wait(99.5, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "00",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=1)
    engine.wait(20, allowed_message=False)
    engine.send_did("WRITE", "退网通知060B", 退网设备=config["测试设备地址"])

    engine.add_doc_info("3、如果10s重试上报过程中，收到网关应答，不再进行100s")
    set_gw_info()  # 设置网关PANID信息，模拟设备入网
    engine.wait(14.5, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "00",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=1)
    engine.wait(9.5, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "00",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=1, ack=True)
    engine.wait(120, allowed_message=False)
    engine.send_did("WRITE", "退网通知060B", 退网设备=config["测试设备地址"])

    engine.add_doc_info("测试添加网关后，添加上报前，是否可以正常被控制通断")
    set_gw_info()  # 设置网关PANID信息，模拟设备入网
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(1)
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(1)
    engine.send_did("WRITE", "继电器翻转C018", "01")
    engine.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(1)
    engine.send_did("WRITE", "继电器翻转C018", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")

    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "00",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=15, ack=True)
    # 测试入网结束，再次测试开关控制模块添加入网，需要发送退网通知060B
    engine.send_did("WRITE", "退网通知060B", 退网设备=config["测试设备地址"])

    engine.add_doc_info("5、测试添加上报重试的过程中，是否可以正常被控制通断")
    set_gw_info()  # 设置网关PANID信息，模拟设备入网
    engine.wait(14.5, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "00",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=1)
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(1)
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(1)
    engine.send_did("WRITE", "继电器翻转C018", "01")
    engine.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(1)
    engine.send_did("WRITE", "继电器翻转C018", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")

    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "00",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=10)
    engine.wait(20)
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(10)
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(10)
    engine.send_did("WRITE", "继电器翻转C018", "01")
    engine.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(10)
    engine.send_did("WRITE", "继电器翻转C018", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "00",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=100)
    engine.wait(20, allowed_message=False)
    # 测试入网结束，再次测试开关控制模块添加入网，需要发送退网通知060B
    engine.send_did("WRITE", "退网通知060B", 退网设备=config["测试设备地址"])

    # 测试开关控制模块处于不同的初始状态，添加上报的内容是否正确，
    # 继电器处于断开上述已验证，再次测试继电器处于闭合的状态，进行添加上报测试
    engine.add_doc_info("6、继电器处于断开上述已验证，再次测试继电器处于闭合的状态，进行添加上报测试；")
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    set_gw_info()  # 设置网关PANID信息，模拟设备入网
    engine.wait(14.5, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "01",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=1, ack=True)
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")


def test_上电上报():
    """
    03_上电上报测试
    上电上报就算公式：延时时间1分钟（网关重启组网时间）+ rand 秒，其中rand=sid% 100。
    1、测试测试sid > 100的情况，sid = 120的情况下，测试网关正常应答的情况
    2、测试测试sid < 100的情况，sid = 8的情况下，测试网关正常应答的情况
    3、测试上报重发机制，收不到网关应答，进行10s、100s重试，重试结束则本次添加上报结束
    4、如果10s重试上报过程中，收到网关应答，不再进行100重试上报
    """

    engine.add_doc_info("1、测试测试sid > 100的情况，sid = 120的情况下，测试网关正常应答的情况")
    config = engine.get_config()
    engine.send_local_msg("设置PANID", 1100)
    engine.expect_local_msg("确认")
    engine.send_did("WRITE", "载波芯片注册信息0603",
                    aid=config["测试设备地址"],
                    panid=1100,
                    pw=config["设备PWD000A"],
                    device_gid=config["抄控器默认源地址"],
                    sid=120)
    engine.expect_did("WRITE", "载波芯片注册信息0603", "** ** ** ** ** **")
    engine.wait(14.5, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "**",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=1)
    # 前端工装断电重启，模拟上电上报
    engine.send_did("WRITE", "通断操作C012", "01", taid=778856)
    engine.wait(seconds=5)
    engine.send_did("WRITE", "通断操作C012", "81", taid=778856)
    # sid = 120时，上电上报时间 = 60+sid% 100 =80s
    engine.wait(79, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "**",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=2, ack=True)  # 预留1s的误差
    engine.send_did("WRITE", "退网通知060B", 退网设备=config["测试设备地址"])

    engine.add_doc_info("测试sid < 100的情况，sid = 8的情况下，测试网关正常应答的情况")
    set_gw_info()
    engine.wait(14.5, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "**",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=1)
    # 前端工装断电重启，模拟上电上报
    engine.send_did("WRITE", "通断操作C012", "01", taid=778856)
    engine.wait(seconds=5)
    engine.send_did("WRITE", "通断操作C012", "81", taid=778856)
    # sid = 8时，上电上报时间 = 60+sid% 100 =68s
    engine.wait(67, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "**",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=2, ack=True)  # 预留1s的误差

    # 测试上报重发机制，收不到网关应答，进行10s、100s重试，重试结束则本次添加上报结束
    engine.add_doc_info("测试上报重发机制，收不到网关应答，进行10s、100s重试，重试结束则本次添加上报结束")
    # 前端工装断电重启，模拟上电上报
    engine.send_did("WRITE", "通断操作C012", "01", taid=778856)
    engine.wait(seconds=5)
    engine.send_did("WRITE", "通断操作C012", "81", taid=778856)
    # sid = 8时，上电上报时间 = 60+sid% 100 =68s
    engine.wait(67, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "**",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=2)  # 预留1s的误差
    engine.wait(9.5, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "**",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=1)
    engine.wait(99.5, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "**",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=1)
    engine.wait(20, allowed_message=False)

    # 如果10s重试上报过程中，收到网关应答，不再进行100重试上报
    engine.add_doc_info("如果10s重试上报过程中，收到网关应答，不再进行100重试上报")
    # 前端工装断电重启，模拟上电上报
    engine.send_did("WRITE", "通断操作C012", "01", taid=778856)
    engine.wait(seconds=5)
    engine.send_did("WRITE", "通断操作C012", "81", taid=778856)
    # sid = 8时，上电上报时间 = 60+sid% 100 =68s
    engine.wait(67, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "**",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=2)  # 预留1s的误差
    engine.wait(9.5, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "**",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=1, ack=True)
    engine.wait(120, allowed_message=False)


def test_配置订阅者():
    """
    04_配置订阅者信息
    1、配置无订阅者，测试开关控制模块是否有上报信息；
    2、配置1个订阅者，测试开关控制模块上报是否正常；
    3、配置2个订阅者，测试开关控制模块上报是否正常；
    4、配置3个订阅者，测试开关控制模块上报是否正常；
    5、测试断电后订阅者信息会丢失；
    6、对于开的设备，重复发开，或者对于关的设备，重复发关的命令，不会重复上报订阅者；
    """
    # 上电配置无订阅者时：使用网关控制后，只回复网关，不上报其他设备
    engine.add_doc_info("上电配置无订阅者时：")
    power_off_test()

    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(10, allowed_message=False)
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(10, allowed_message=False)

    # 配置1个订阅者时：使用网关控制后，回复网关，并上报订阅者
    power_off_test()
    panel01 = set_subscriber("订阅者1", 21)
    # 网关控制
    engine.add_doc_info("网关控制")
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    panel01.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.wait(10, allowed_message=False)
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    panel01.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.wait(10, allowed_message=False)

    # 配置2个订阅者时：使用网关控制后，回复网关，并上报订阅者
    engine.add_doc_info("配置2个订阅者时：")
    power_off_test()
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)

    # 网关控制
    engine.add_doc_info("网关控制")
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    panel01.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.wait(10, allowed_message=False)
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    panel01.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.wait(10, allowed_message=False)
    # 配置3个订阅者时：使用网关控制后，回复网关，并上报订阅者
    engine.add_doc_info("配置3个订阅者时：")
    power_off_test()
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)
    # 网关控制
    engine.add_doc_info("网关控制")
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    panel01.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.wait(10, allowed_message=False)
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    panel01.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.wait(10, allowed_message=False)

    # 测试断电后订阅者信息会丢失，在3个订阅者的基础上，进行断电重启，网关再次控制设备，只上报网关，不上报订阅者；
    power_off_test()
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(10, allowed_message=False)
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(10, allowed_message=False)
    # 对于开的设备，重复发开，或者对于关的设备，重复发关的命令，不会重复上报订阅者；
    engine.add_doc_info("配置3个订阅者时：")
    power_off_test()
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)
    # 网关控制
    engine.add_doc_info("网关控制")
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    panel01.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.wait(10, allowed_message=False)
    engine.add_doc_info("重复控制打开")
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(10, allowed_message=False)

    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    panel01.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.wait(10, allowed_message=False)
    engine.add_doc_info("重复控制关闭")
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(10, allowed_message=False)


def test_订阅者上报顺序测试():
    """
    05_订阅者上报顺序测试
    当存在多个订阅者（大于3个订阅者时），新增的订阅者会替换最早添加的订阅者；
    以订阅1、订阅者2、订阅者3、订阅4进行测试验证
    """
    # 通过断电使开关控制模块的订阅者丢失
    power_off_test()
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(10, allowed_message=False)
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(10, allowed_message=False)
    # 订阅者1、订阅者2、订阅者3依次控制，发现上报的顺序为订阅者1、订阅者2、订阅者3
    # 配置订阅者后，使用网关控制后，回复网关，并上报订阅者
    engine.add_doc_info("配置3个订阅者时：")
    power_off_test()
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)
    # 网关控制
    engine.add_doc_info("网关控制")
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    panel01.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.wait(10, allowed_message=False)
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    panel01.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.wait(10, allowed_message=False)
    # 订阅者4控制一次，发现上报的顺序变成订阅者4、订阅者2、订阅者3
    # 配置订阅者后，使用网关控制后，回复网关，并上报订阅者
    engine.add_doc_info("订阅者4控制一次后：")
    panel04 = set_subscriber("订阅者4", 24)
    # 网关控制
    engine.add_doc_info("网关控制")
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    panel04.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.wait(10, allowed_message=False)
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    panel04.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.wait(10, allowed_message=False)
    # 订阅者1控制一次，发现上报的顺序变成订阅者4、订阅者1、订阅者3
    # 配置订阅者后，使用网关控制后，回复网关，并上报订阅者
    engine.add_doc_info("订阅者1控制一次后：")
    panel01 = set_subscriber("订阅者1", 21)
    # 网关控制
    engine.add_doc_info("网关控制")
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    panel04.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel01.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.wait(10, allowed_message=False)
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    panel04.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel01.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    # 订阅者2控制一次，发现上报的顺序变成订阅者4、订阅者1、订阅者2
    # 配置订阅者后，使用网关控制后，回复网关，并上报订阅者
    engine.add_doc_info("订阅者2控制一次后：")
    panel02 = set_subscriber("订阅者2", 22)
    # 网关控制
    engine.add_doc_info("网关控制")
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    panel04.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel01.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.wait(10, allowed_message=False)
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    panel04.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel01.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    # 订阅者3控制一次，发现上报的顺序变成订阅者3、订阅者1、订阅者2
    # 配置订阅者后，使用网关控制后，回复网关，并上报订阅者
    engine.add_doc_info("订阅者3控制一次后：")
    panel03 = set_subscriber("订阅者3", 23)
    # 网关控制
    engine.add_doc_info("网关控制")
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    panel03.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel01.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.wait(10, allowed_message=False)
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel01.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)


def test_默认参数同时上报设备和网关():
    """
    06_默认参数同时上报设备和网关
    # 1、本地直接控制开关，1.3s后观察到上报订阅者，订阅者回复，上报网关，网关回复，间隔0.2s(仅机械开关控制模块支持)
    # 2、手机客户端单点控制（网关控制）——被控设备状态立即回复网关，状态同步先后上报订阅者
    # 3、手机客户端情景模式控制（网关控制）——被控设备状态按组地址顺序上报，状态同步先后上报订阅者，最后上报网关
    # 4、订阅者01单点控制——被控设备状态立即回复订阅者01，状态同步先后上报订阅者02、订阅者03，最后上报网关
    # 5、订阅者01情景模式控制——被控设备状态按组地址顺序上报，状态同步先后上报订阅者01、订阅者02、订阅者03，最后上报网关
    """
    power_off_test()
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")
    # 配置订阅者3个
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)
    # 1、本地直接控制开关，1.3s后观察到上报订阅者，订阅者回复，上报网关，网关回复，间隔0.2s(仅机械开关控制模块支持)
    # 普通的开关控制模块不支持，本功能暂不测试
    # 2、手机客户端单点控制（网关控制）——被控设备状态立即回复网关，状态同步先后上报订阅者
    engine.add_doc_info("网关单点控制")
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    panel01.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.wait(10, allowed_message=False)

    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    panel01.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.wait(10, allowed_message=False)

    # 3、手机客户端情景模式控制（网关控制）——被控设备状态按组地址顺序上报，状态同步先后上报订阅者，最后上报网关
    engine.send_did("WRITE", "通断操作C012", "81", taid=0xFFFFFFFF, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
    panel01.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "01",
                             "导致状态改变的控制设备AIDC01A", config["抄控器默认源地址"], timeout=2, ack=True)
    engine.wait(10, allowed_message=False)

    engine.send_did("WRITE", "通断操作C012", "00", taid=0xFFFFFFFF, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
    panel01.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "00",
                             "导致状态改变的控制设备AIDC01A", config["抄控器默认源地址"], timeout=2, ack=True)
    engine.wait(10, allowed_message=False)

    # 4、订阅者01单点控制——被控设备状态立即回复订阅者01，状态同步先后上报订阅者02、订阅者03，最后上报网关
    engine.add_doc_info("订阅者01单点控制")
    panel01.send_did("WRITE", "通断操作C012", "81")
    panel01.expect_did("WRITE", "通断操作C012", "01")

    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "01",
                             "导致状态改变的控制设备AIDC01A", panel01.src, timeout=2, ack=True)
    engine.wait(10, allowed_message=False)

    engine.add_doc_info("订阅者01单点控制")
    panel01.send_did("WRITE", "通断操作C012", "01")
    panel01.expect_did("WRITE", "通断操作C012", "00")

    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "00",
                             "导致状态改变的控制设备AIDC01A", panel01.src, timeout=2, ack=True)
    engine.wait(10, allowed_message=False)

    # 5、订阅者01情景模式控制——被控设备状态按组地址顺序上报，状态同步先后上报订阅者01、订阅者02、订阅者03，最后上报网关
    panel01.send_did("WRITE", "通断操作C012", "81", taid=0xFFFFFFFF, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
    panel01.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.expect_multi_dids("REPORT", "通断操作C012", "01", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=2, ack=True)
    engine.wait(10, allowed_message=False)

    panel01.send_did("WRITE", "通断操作C012", "00", taid=0xFFFFFFFF, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
    panel01.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.expect_multi_dids("REPORT", "通断操作C012", "00", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=2, ack=True)
    engine.wait(10, allowed_message=False)


def test_不上报():
    """
    07_不上报
    # 1、本地直接控制开关，不上报订阅者和网关
    # 2、手机客户端单点控制（网关控制）——被控设备状态立即回复网关，状态同步不上报订阅者
    # 3、手机客户端情景模式控制（网关控制）——不上报订阅者和网关
    # 4、订阅者01单点控制——被控设备状态立即回复订阅者01，不上报订阅者和网关
    # 5、订阅者01情景模式控制——不上报订阅者和网关
    """
    power_off_test()
    # 设置为不上报模式
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="无上报")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="无上报")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="无上报")

    # 配置订阅者3个
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)
    # 1、本地直接控制开关，不上报订阅者和网关(仅机械开关控制模块支持)
    # 普通的开关控制模块不支持，本功能暂不测试
    # 2、手机客户端单点控制（网关控制）——被控设备状态立即回复网关，状态同步不上报订阅者
    engine.add_doc_info("网关单点控制")
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(10, allowed_message=False)
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(10, allowed_message=False)
    # 3、手机客户端情景模式控制（网关控制）——不上报订阅者和网关
    engine.send_did("WRITE", "通断操作C012", "81", taid=0xFFFFFFFF, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
    engine.wait(10, allowed_message=False)

    engine.send_did("WRITE", "通断操作C012", "01", taid=0xFFFFFFFF, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
    engine.wait(10, allowed_message=False)

    # 4、订阅者01单点控制——被控设备状态立即回复订阅者01，不上报订阅者和网关
    engine.add_doc_info("订阅者01单点控制")
    panel01.send_did("WRITE", "通断操作C012", "81")
    panel01.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(10, allowed_message=False)

    engine.add_doc_info("订阅者01单点控制")
    panel01.send_did("WRITE", "通断操作C012", "01")
    panel01.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(10, allowed_message=False)

    # 5、订阅者01情景模式控制——不上报订阅者和网关
    panel01.send_did("WRITE", "通断操作C012", "81", taid=0xFFFFFFFF, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
    engine.wait(10, allowed_message=False)

    panel01.send_did("WRITE", "通断操作C012", "01", taid=0xFFFFFFFF, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
    engine.wait(10, allowed_message=False)


def test_只上报网关():
    """
    08_只上报网关
    # 1、本地直接控制开关，不上报订阅者，只上报网关(仅机械开关控制模块支持)
    # 2、手机客户端单点控制（网关控制）——被控设备状态立即回复网关，状态同步不上报订阅者
    # 3、手机客户端情景模式控制（网关控制）——被控设备状态按组地址顺序上报，状态同步不上报订阅者，只上报网关
    # 4、订阅者01单点控制——被控设备状态立即回复订阅者01，状态同步不上报订阅者02、订阅者03，只上报网关
    # 5、订阅者01情景模式控制——被控设备状态按组地址顺序上报，状态同步不上报订阅者01、订阅者02、订阅者03，只上报网关
    """
    power_off_test()
    # 设置为只上报网关模式
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")

    # 配置订阅者3个
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)
    # 1、本地直接控制开关，不上报订阅者，只上报网关(仅机械开关控制模块支持)
    # 2、手机客户端单点控制（网关控制）——被控设备状态立即回复网关，状态同步不上报订阅者
    engine.add_doc_info("网关单点控制")
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(10, allowed_message=False)
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(10, allowed_message=False)
    # 3、手机客户端情景模式控制（网关控制）——被控设备状态按组地址顺序上报，状态同步不上报订阅者，只上报网关
    engine.send_did("WRITE", "通断操作C012", "81", taid=0xFFFFFFFF, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "01",
                             "导致状态改变的控制设备AIDC01A", config["抄控器默认源地址"], timeout=2, ack=True)
    engine.wait(10, allowed_message=False)

    engine.send_did("WRITE", "通断操作C012", "00", taid=0xFFFFFFFF, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "00",
                             "导致状态改变的控制设备AIDC01A", config["抄控器默认源地址"], timeout=2, ack=True)
    engine.wait(10, allowed_message=False)

    # 4、订阅者01单点控制——被控设备状态立即回复订阅者01，状态同步不上报订阅者02、订阅者03，只上报网关
    engine.add_doc_info("订阅者01单点控制")
    panel01.send_did("WRITE", "通断操作C012", "81")
    panel01.expect_did("WRITE", "通断操作C012", "01")
    engine.expect_multi_dids("REPORT", "通断操作C012", "01", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=2, ack=True)
    engine.wait(10, allowed_message=False)

    engine.add_doc_info("订阅者01单点控制")
    panel01.send_did("WRITE", "通断操作C012", "01")
    panel01.expect_did("WRITE", "通断操作C012", "00")
    engine.expect_multi_dids("REPORT", "通断操作C012", "00", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=2, ack=True)
    engine.wait(10, allowed_message=False)
    # 5、订阅者01情景模式控制——被控设备状态按组地址顺序上报，状态同步不上报订阅者01、订阅者02、订阅者03，只上报网关
    panel01.send_did("WRITE", "通断操作C012", "81", taid=0xFFFFFFFF, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
    engine.expect_multi_dids("REPORT", "通断操作C012", "01", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=2, ack=True)
    engine.wait(10, allowed_message=False)

    panel01.send_did("WRITE", "通断操作C012", "00", taid=0xFFFFFFFF, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
    engine.expect_multi_dids("REPORT", "通断操作C012", "00", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=2, ack=True)
    engine.wait(10, allowed_message=False)


def test_只上报设备():
    """
    09_只上报设备
    # 1、本地直接控制开关，1.3s后观察到上报订阅者，订阅者回复，不上报网关(仅机械开关控制模块支持)
    # 2、手机客户端单点控制（网关控制）——被控设备状态立即回复网关，状态同步先后上报订阅者
    # 3、手机客户端情景模式控制（网关控制）——被控设备状态按组地址顺序上报，状态同步先后上报订阅者，不上报网关
    # 4、订阅者01单点控制——被控设备状态立即回复订阅者01，状态同步先后上报订阅者02、订阅者03，不上报网关
    # 5、订阅者01情景模式控制——被控设备状态按组地址顺序上报，状态同步先后上报订阅者01、订阅者02、订阅者03，不上报网关
    """
    power_off_test()
    # 设置为只上报网关模式
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报设备")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报设备")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报设备")
    # 配置订阅者3个
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)
    # 1、本地直接控制开关，1.3s后观察到上报订阅者，订阅者回复，不上报网关(仅机械开关控制模块支持)
    # 2、手机客户端单点控制（网关控制）——被控设备状态立即回复网关，状态同步先后上报订阅者
    engine.add_doc_info("网关单点控制")
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    panel01.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.wait(10, allowed_message=False)
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    panel01.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.wait(10, allowed_message=False)
    # 3、手机客户端情景模式控制（网关控制）——被控设备状态按组地址顺序上报，状态同步先后上报订阅者，不上报网关
    engine.send_did("WRITE", "通断操作C012", "81", taid=0xFFFFFFFF, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
    panel01.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.wait(10, allowed_message=False)

    engine.send_did("WRITE", "通断操作C012", "00", taid=0xFFFFFFFF, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
    panel01.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.wait(10, allowed_message=False)

    # 4、订阅者01单点控制——被控设备状态立即回复订阅者01，状态同步先后上报订阅者02、订阅者03，不上报网关
    engine.add_doc_info("订阅者01单点控制")
    panel01.send_did("WRITE", "通断操作C012", "81")
    panel01.expect_did("WRITE", "通断操作C012", "01")
    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.wait(10, allowed_message=False)

    engine.add_doc_info("订阅者01单点控制")
    panel01.send_did("WRITE", "通断操作C012", "01")
    panel01.expect_did("WRITE", "通断操作C012", "00")
    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.wait(10, allowed_message=False)
    # 5、订阅者01情景模式控制——被控设备状态按组地址顺序上报，状态同步先后上报订阅者01、订阅者02、订阅者03，不上报网关
    panel01.send_did("WRITE", "通断操作C012", "81", taid=0xFFFFFFFF, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
    panel01.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.wait(10, allowed_message=False)

    panel01.send_did("WRITE", "通断操作C012", "00", taid=0xFFFFFFFF, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
    panel01.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.wait(10, allowed_message=False)


def test_网关无应答时设备上报的重试机制():
    """
    10_网关无应答时设备上报的重试机制
    在默认参数同时上报设备和网关情况下测试：
    1、测试正常情况，网关正常应答
    2、测试网关不应答异常情况，进行10s、100s重试，重试结束则本次添加上报结束
    3、如果10s重试上报过程中，收到网关应答，不再进行100重试上报
    4、上报过程中，收到新的控制命令，本次重试上报结束，开始新的上报流程
    5、如果10s重试上报过程中，收到新的控制命令，本次重试上报结束，开始新的上报流程
    6、如果100s重试上报过程中，收到新的控制命令，本次重试上报结束，开始新的上报流程
    """
    power_off_test()
    # 设置为同时上报设备和网关模式
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")
    # 配置订阅者3个
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)
    # 1、测试正常情况，网关正常应答
    engine.add_doc_info("订阅者01单点控制")
    panel01.send_did("WRITE", "通断操作C012", "81")
    panel01.expect_did("WRITE", "通断操作C012", "01")

    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.expect_multi_dids("REPORT", "通断操作C012", "01", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=2, ack=True)
    engine.wait(10, allowed_message=False)

    engine.add_doc_info("订阅者01单点控制")
    panel01.send_did("WRITE", "通断操作C012", "01")
    panel01.expect_did("WRITE", "通断操作C012", "00")

    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.expect_multi_dids("REPORT", "通断操作C012", "00", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=1, ack=True)
    engine.wait(10, allowed_message=False)
    # 2、测试网关不应答异常情况，进行10s、100s重试，重试结束则本次添加上报结束
    engine.add_doc_info("订阅者01单点控制")
    panel01.send_did("WRITE", "通断操作C012", "81")
    panel01.expect_did("WRITE", "通断操作C012", "01")

    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.expect_multi_dids("REPORT", "通断操作C012", "01", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=1)
    engine.wait(9.5, allowed_message=False)
    engine.expect_multi_dids("REPORT", "通断操作C012", "01", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=1)
    engine.wait(99.5, allowed_message=False)
    engine.expect_multi_dids("REPORT", "通断操作C012", "01", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=1)
    engine.wait(100, allowed_message=False)

    engine.add_doc_info("订阅者01单点控制")
    panel01.send_did("WRITE", "通断操作C012", "01")
    panel01.expect_did("WRITE", "通断操作C012", "00")

    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.expect_multi_dids("REPORT", "通断操作C012", "00", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=1)
    engine.wait(9.5, allowed_message=False)
    engine.expect_multi_dids("REPORT", "通断操作C012", "00", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=1)
    engine.wait(99.5, allowed_message=False)
    engine.expect_multi_dids("REPORT", "通断操作C012", "00", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=1)
    engine.wait(100, allowed_message=False)

    # 3、如果10s重试上报过程中，收到网关应答，不再进行100重试上报
    engine.add_doc_info("订阅者01单点控制")
    panel01.send_did("WRITE", "通断操作C012", "81")
    panel01.expect_did("WRITE", "通断操作C012", "01")

    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.expect_multi_dids("REPORT", "通断操作C012", "01", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=1)
    engine.wait(9.5, allowed_message=False)
    engine.expect_multi_dids("REPORT", "通断操作C012", "01", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=1, ack=True)
    engine.wait(120, allowed_message=False)

    engine.add_doc_info("订阅者01单点控制")
    panel01.send_did("WRITE", "通断操作C012", "01")
    panel01.expect_did("WRITE", "通断操作C012", "00")

    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.expect_multi_dids("REPORT", "通断操作C012", "00", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=1)
    engine.wait(9.5, allowed_message=False)
    engine.expect_multi_dids("REPORT", "通断操作C012", "01", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=1, ack=True)
    engine.wait(120, allowed_message=False)

    # 4、上报过程中，收到新的控制命令，本次重试上报结束，开始新的上报流程
    engine.add_doc_info("订阅者01单点控制")
    panel01.send_did("WRITE", "通断操作C012", "81")
    panel01.expect_did("WRITE", "通断操作C012", "01")

    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.add_doc_info("上报订阅者后，被控制")
    panel01.send_did("WRITE", "通断操作C012", "01")
    panel01.expect_did("WRITE", "通断操作C012", "00")

    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.expect_multi_dids("REPORT", "通断操作C012", "00", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=1, ack=True)
    engine.wait(10, allowed_message=False)

    # 5、如果10s重试上报过程中，收到新的控制命令，本次重试上报结束，开始新的上报流程
    engine.add_doc_info("订阅者01单点控制")
    panel01.send_did("WRITE", "通断操作C012", "81")
    panel01.expect_did("WRITE", "通断操作C012", "01")

    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.expect_multi_dids("REPORT", "通断操作C012", "01", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=1)
    engine.wait(5, allowed_message=False)
    engine.add_doc_info("如果10s重试上报过程中，收到新的控制命令，本次重试上报结束，开始新的上报流程")
    panel01.send_did("WRITE", "通断操作C012", "01")
    panel01.expect_did("WRITE", "通断操作C012", "00")

    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.expect_multi_dids("REPORT", "通断操作C012", "00", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=1)
    engine.wait(9.5, allowed_message=False)
    engine.expect_multi_dids("REPORT", "通断操作C012", "00", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=1)
    engine.wait(99.5, allowed_message=False)
    engine.expect_multi_dids("REPORT", "通断操作C012", "00", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=1)
    engine.wait(100, allowed_message=False)

    # 6、如果100s重试上报过程中，收到新的控制命令，本次重试上报结束，开始新的上报流程

    engine.add_doc_info("订阅者01单点控制")
    panel01.send_did("WRITE", "通断操作C012", "81")
    panel01.expect_did("WRITE", "通断操作C012", "01")

    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.expect_multi_dids("REPORT", "通断操作C012", "01", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=1)
    engine.wait(9.5, allowed_message=False)
    engine.expect_multi_dids("REPORT", "通断操作C012", "01", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=1)
    engine.wait(50, allowed_message=False)

    engine.add_doc_info("如果100s重试上报过程中，收到新的控制命令，本次重试上报结束，开始新的上报流程")
    panel01.send_did("WRITE", "通断操作C012", "01")
    panel01.expect_did("WRITE", "通断操作C012", "00")

    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.expect_multi_dids("REPORT", "通断操作C012", "00", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=1)
    engine.wait(9.5, allowed_message=False)
    engine.expect_multi_dids("REPORT", "通断操作C012", "00", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=1)
    engine.wait(99.5, allowed_message=False)
    engine.expect_multi_dids("REPORT", "通断操作C012", "00", "导致状态改变的控制设备AIDC01A", panel01.src, timeout=1)
    engine.wait(100, allowed_message=False)


def test_广播报文控制测试():
    """
    11_广播报文控制测试
    暂不支持
    1、组地址按位组合
    2、组地址按单字节组合
    3、组地址按双字节组合
    4、存在多个组地址的情况，组地址在前
    5、存在多个组地址的情况，组地址在后
    6、不同组地址混合 按单字节+按双字节+按位组合
    7、模拟220字节超长情景模式报文测试
    """
    engine.add_doc_info("测试前准备工作，配置3个订阅者")
    # 配置订阅者3个
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)

    engine.add_doc_info("1、组地址按位组合")
    engine.send_did("WRITE", "通断操作C012", "81", taid=0xFFFFFFFF, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
    panel01.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "01",
                             "导致状态改变的控制设备AIDC01A", config["抄控器默认源地址"], timeout=2, ack=True)
    engine.wait(10, allowed_message=False)

    engine.send_did("WRITE", "通断操作C012", "00", taid=0xFFFFFFFF, gids=[7, 8, 9, 10, 11], gid_type="BIT1")
    panel01.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "00",
                             "导致状态改变的控制设备AIDC01A", config["抄控器默认源地址"], timeout=2, ack=True)
    engine.wait(10, allowed_message=False)

    engine.add_doc_info("2、组地址按单字节组合")
    engine.send_did("WRITE", "通断操作C012", "81", taid=0xFFFFFFFF, gids=[7, 8, 9, 10, 11], gid_type="U8")
    panel01.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "01",
                             "导致状态改变的控制设备AIDC01A", config["抄控器默认源地址"], timeout=2, ack=True)
    engine.wait(10, allowed_message=False)

    engine.send_did("WRITE", "通断操作C012", "00", taid=0xFFFFFFFF, gids=[7, 8, 9, 10, 11], gid_type="U8")
    panel01.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "00",
                             "导致状态改变的控制设备AIDC01A", config["抄控器默认源地址"], timeout=2, ack=True)
    engine.wait(10, allowed_message=False)

    engine.add_doc_info("3、组地址按双字节组合")
    engine.send_did("WRITE", "通断操作C012", "81", taid=0xFFFFFFFF, gids=[7, 8, 9, 10, 11], gid_type="U16")
    panel01.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "01", timeout=2)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "01",
                             "导致状态改变的控制设备AIDC01A", config["抄控器默认源地址"], timeout=2, ack=True)
    engine.wait(10, allowed_message=False)

    engine.send_did("WRITE", "通断操作C012", "00", taid=0xFFFFFFFF, gids=[7, 8, 9, 10, 11], gid_type="U16")
    panel01.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel02.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    panel03.expect_did("NOTIFY", "通断操作C012", "00", timeout=2)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "00",
                             "导致状态改变的控制设备AIDC01A", config["抄控器默认源地址"], timeout=2, ack=True)
    engine.wait(10, allowed_message=False)

    engine.add_doc_info("4、存在多个组地址的情况，组地址在前")
    # 暂不支持
    engine.add_doc_info("6、不同组地址混合 按单字节+按双字节+按位组合")
    engine.add_doc_info("7、模拟220字节超长情景模式报文测试")


# def test_test():
#     """
#     test
#     """
#     pass
