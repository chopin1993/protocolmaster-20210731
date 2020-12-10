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


