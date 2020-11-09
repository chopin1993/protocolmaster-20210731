import engine

测试组说明="测试状态同步代码"

def start_report():
    r"4aid+2panid+2pw+4gid+2sid"
    config = engine.get_config()
    engine.send_local_msg("设置PANID", config["panid"])
    engine.expect_local_msg("确认")
    engine.send_did("WRITE", "载波芯片注册信息",
                    aid=config["测试设备地址"],
                    panid=config["panid"],
                    pw=config["设备密码"],
                    gid=1,
                    sid=1)
    engine.expect_did("WRITE", "载波芯片注册信息", "** ** ** ** ** **")


def test_gateway_report():
    """
    组网上报
    测试设备组网上报功能。
    1. 将设备上报模式设置为上报网关
    2. 发起模拟设备组网命令。
    3. 设备会在65s内上报开关状态
    4. 如果没有收到回复，设备会重发两次
    5. 收到回复时，设备便不再重发
    """
    config = engine.get_config()
    engine.send_did("WRITE", "主动上报使能标志",传感器类型="开关", 上报命令="上报网关")
    engine.expect_did("WRITE", "主动上报使能标志", 传感器类型="开关", 上报命令="上报网关")

    start_report()
    engine.add_doc_info("设备会在65s内第一次上报")
    engine.expect_multi_dids("REPORT", "通断操作C012", "**","导致状态改变的控制设备AID", "** ** ** **", timeout=65)
    engine.add_doc_info("设备会在100s内第二次上报")
    engine.wait(50, expect_no_message=True)
    engine.expect_multi_dids("REPORT", "通断操作C012", "**","导致状态改变的控制设备AID", "** ** ** **", timeout=200)
    engine.add_doc_info("设备会在150s内第三次上报")
    engine.wait(50, expect_no_message=True)
    engine.expect_multi_dids("REPORT", "通断操作C012", "**", "导致状态改变的控制设备AID", "** ** ** **", timeout=300)

    engine.add_doc_info("上报收到回复之后，便不会重发")
    start_report()
    engine.expect_multi_dids("REPORT", "通断操作C012", "**", "导致状态改变的控制设备AID", "** ** ** **", timeout=65, ack=True)
    engine.wait(250, expect_no_message=True)


def test_subscribe_report():
    """
    只上报订阅者
    测试设备只上报订阅者模式。本测试需要经过如下几步：
    1. 首先将设备的上报模式设置为上报设备，
    2. 使用面板控制设备，面板就会自动成为设备的订阅者。
    3. 通过其他地址控制设备，设备会自动将状态信息上报给面板
    """
    engine.send_did("WRITE", "主动上报使能标志", 传感器类型="开关", 上报命令="上报设备")
    engine.expect_did("WRITE", "主动上报使能标志", 传感器类型="开关", 上报命令="上报设备")

    engine.add_doc_info("面板控制设备之后，会自动成为设备的订阅者，其他设备在控制开关控制器，开关控制器回向面板上报")
    panel = engine.create_role("订阅者1", 3)
    panel.send_did("WRITE", "通断操作C012", "01")
    panel.expect_did("WRITE","通断操作C012","00")
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    panel.expect_did("REPORT", "通断操作C012","01",timeout=15,ack=True)
