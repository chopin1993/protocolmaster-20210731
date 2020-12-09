import engine

device_type = "FF FF 02 00 11 02 01 00"
def test_software_version():
    """
    did测试
    did可以为字符串，可以是Number，也可以是字符串形式的Number
    """
    engine.send_did("READ", "设备类型0001")
    match_pattern = "** ** ** ** ** ** ** **"
    engine.expect_did("READ", "设备类型0001", match_pattern)

    engine.send_did("read", 0x0001)
    engine.expect_did("READ", "设备类型0001", match_pattern)

    engine.send_did("READ", "0x0001")
    engine.expect_did("READ", "设备类型0001", match_pattern)

    engine.send_did("READ", "0001")
    engine.expect_did("READ", "设备类型0001", "** ** ** ** ** ** ** **")

def test_device_type():
    """
    设备类型测试
    did可以为字符串，可以是Number，也可以是字符串形式的Number
    """
    engine.send_did("READ", "设备类型0001")
    engine.expect_did("READ", "设备类型0001", device_type)


def test_did_para():
    """
    参数测试
    参数可以使用hex字符串自组报文，如果有多个单元，可以使用key value方式
    """
    #参数可以使用hex字符串自组报文
    engine.send_did("WRITE", "主动上报使能标志D005", "00 00")
    engine.expect_did("WRITE", "主动上报使能标志D005",
                      传感器类型="未知", 上报命令=0)


    # 如果有多个单元，可以使用key value方式
    engine.send_did("WRITE", "主动上报使能标志D005",  传感器类型=0, 上报命令=0)
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型=0, 上报命令=0)


def test_r_string():
    """
    字符串反转
    """
    engine.send_did("READ", "0004")
    engine.expect_did("READ", "0004", "SSC1663-ADPT-V30A012")

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

