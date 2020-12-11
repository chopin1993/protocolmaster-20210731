import engine


def test_input():
    """
    输入测试-int
    """
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")

    engine.set_device_sensor_status("按键输入", 1)
    engine.wait(3)
    engine.expect_device_output_status("继电器输出", 0)

    engine.set_device_sensor_status("按键输入", "短按")
    engine.wait(3)


def test_input2():
    """
    输入测试-hexstr
    """
    engine.set_device_sensor_status("按键输入", 0x02)
    engine.wait(3)
    engine.set_device_sensor_status("按键输入", "长按")
    engine.wait(3)


def test_fail():
    """
    失败测试-传感器失败
    """
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    engine.expect_device_output_status("继电器输出", 1)



def test_debug_mode():
    """
    调试模式
    """
    # 触发SWB总线探测
    # 系统复位
    # 清除系统所有信息
    config = engine.get_config()
    engine.send_did("WRITE", "自动测试FC00", 密码=config["设备密码"], 自动测试命令="触发SWB总线探测")
    engine.expect_did("WRITE", "自动测试FC00", 密码=config["设备密码"], 自动测试命令="触发SWB总线探测")

def test_reset_mode():
    """
    调试模式恢复出厂
    """
    config = engine.get_config()
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    engine.send_did("WRITE", "自动测试FC00", 密码=config["设备密码"], 自动测试命令="清除系统所有信息")
    engine.expect_did("WRITE", "自动测试FC00", 密码=config["设备密码"], 自动测试命令="清除系统所有信息")
    engine.wait(15)
    engine.expect_device_output_status("继电器输出", 0)


def test_cross_zero():
    "测试过零检测"
    engine.expect_cross_zero_status(0,0)


def test_resend():
    "重发测试"
    engine.wait(10, tips="请断开监测器，测试重发")
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")


def start_report():
    r"4aid+2panid+2pw+4gid+2sid"
    config = engine.get_config()
    engine.send_did("WRITE", "退网通知060B", 退网设备=config["测试设备地址"])
    engine.wait(1)
    engine.send_local_msg("设置PANID", 0)
    engine.expect_local_msg("确认")
    engine.send_did("WRITE", "载波芯片注册信息0603",
                    aid=config["测试设备地址"],
                    panid=0,
                    pw=config["设备密码"],
                    device_gid=config["抄控器默认源地址"],
                    sid=1)
    engine.expect_did("WRITE", "载波芯片注册信息0603", "** ** ** ** ** **",check_seq=False)

def test_spi_input():
    "自动捕捉spi的报文输出"
    engine.report_check_enable_all(True)
    start_report()
    engine.wait(5, tips="请断开抄控器")
    engine.expect_multi_dids("REPORT", "通断操作C012", "**", "导致状态改变的控制设备AIDC01A", "** ** ** **", timeout=20,ack=True)
    engine.wait(20,allowed_message=False)
    engine.report_check_enable_all(False)

