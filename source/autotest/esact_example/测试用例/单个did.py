import engine

def test_software_version():
    """
    did测试
    did可以为字符串，可以是Number，也可以是字符串形式的Number
    """
    engine.send_did("READ", "设备描述信息设备制造商")
    engine.expect_did("READ", "设备描述信息设备制造商", "ESACT-1A(v1.4)-20171020")

    engine.send_did("read", 0x0003)
    engine.expect_did("READ", "设备描述信息设备制造商", "ESACT-1A(v1.4)-20171020")

    engine.send_did("READ", "0x0003")
    engine.expect_did("READ", "设备描述信息设备制造商", "ESACT-1A(v1.4)-20171020")

    engine.send_did("READ", "0003")
    engine.expect_did("READ", "设备描述信息设备制造商", "ESACT-1A(v1.4)-20171020")


def test_did_para():
    """
    参数测试
    """
    #参数可以使用hex字符串写死
    engine.send_did("WRITE", "主动上报使能标志", "00 00")
    engine.expect_did("WRITE", "主动上报使能标志", 传感器类型="开关", 上报命令=0)


    # 如果有多个单元，可以使用key value方式
    engine.send_did("WRITE", "主动上报使能标志",  传感器类型=0, 上报命令=0)
    engine.expect_did("WRITE", "主动上报使能标志", 传感器类型=0, 上报命令=0)


