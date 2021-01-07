import engine

def clear_gw_info():
    r"4aid+2panid+2pw+4gid+2sid"
    config = engine.get_config()
    engine.send_local_msg("设置PANID", 0)
    engine.expect_local_msg("确认")
    engine.send_did("WRITE", "载波芯片注册信息0603",
                    aid=config["测试设备地址"],
                    panid=0,
                    pw=config["设备PWD000A"],
                    device_gid=config["抄控器默认源地址"],
                    sid=1)
    engine.expect_did("WRITE", "载波芯片注册信息0603", "** ** ** ** ** **",check_seq=False)
    engine.wait(10)


def test_device_search():
    """
    设备搜索测试
    """
    clear_gw_info()

    config = engine.get_config()

    engine.send_did("SEARCH", "APP设备搜索0008",
                    taid=0xffffffff,gid_type="U8",gids=[0],
                    搜索类型="未注册节点", 搜索时间=14, 设备类型="ff ff ff ff")
    engine.expect_multi_dids("SEARCH", "SN0007","32 01 10 10 ** ** ** ** ** ** ** **",
                                       "DKEY0005", "0000DZO9",
                                       "设备PWD000A",config["设备密码"],
                                       "设备描述信息设备制造商0003",config["测试程序名称"],
                                       timeout=20)

    engine.send_did("SEARCH", "APP设备搜索0008",
                    taid=0xffffffff,gid_type="U8",gids=[0],
                    搜索类型="未注册节点", 搜索时间=14, 设备类型="32 01 10 10")
    engine.expect_multi_dids("SEARCH", "SN0007","32 01 10 10 ** ** ** ** ** ** ** **",
                                       "DKEY0005", "0000DZO9",
                                       "设备PWD000A",config["设备密码"],
                                       "设备描述信息设备制造商0003",config["测试程序名称"],
                                       timeout=20)





def test_device_show():
    """
    设备指示
    发送指示命令，验证设备的响应动作是否与要求一致。
    设备指示具体指示动作为第一路继电器翻转，1s变换一次状态，持续6s，设备指示过程中不允许载波通信，本地按键无效。
    """
    engine.send_did("WRITE", "APP设备指示0009", "")
    engine.expect_did("WRITE", "APP设备指示0009", "")
    engine.wait(6)
    clear_gw_info()

def test_clear_getwar_info():
    "清理抄控器和设备网关信息"
    clear_gw_info()