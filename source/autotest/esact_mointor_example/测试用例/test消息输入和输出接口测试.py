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

