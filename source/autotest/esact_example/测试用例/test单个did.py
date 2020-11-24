import engine

def test_software_version():
    """
    did测试
    did可以为字符串，可以是Number，也可以是字符串形式的Number
    """
    engine.send_did("READ", "设备类型0001")
    engine.expect_did("READ", "设备类型0001", "FF FF 18 00 01 00 01 00")

    engine.send_did("read", 0x0001)
    engine.expect_did("READ", "设备类型0001", "FF FF 18 00 01 00 01 00")

    engine.send_did("READ", "0x0001")
    engine.expect_did("READ", "设备类型0001", "FF FF 18 00 01 00 01 00")

    engine.send_did("READ", "0001")
    engine.expect_did("READ", "设备类型0001", "** ** ** ** ** ** ** **")



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
    engine.expect_did("READ", "0004", "SSC1663-ADPT-V30A014")

