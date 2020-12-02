# encoding:utf-8
# 导入测试引擎
import engine

def clear_gw_info():
    """
    清除网关PANID信息，模拟出厂设备
    r"4aid+2panid+2pw+4gid+2sid"
    """
    config = engine.get_config()
    # 发送退网报文
    engine.send_did("WRITE", "退网通知060B", 退网设备=config["测试设备地址"])

    engine.send_local_msg("设置PANID", 0)
    engine.expect_local_msg("确认")
    engine.wait(1)
    engine.send_did("WRITE", "载波芯片注册信息0603",
                    aid=config["测试设备地址"],
                    panid=0,
                    pw=config["设备PWD000A"],
                    device_gid=config["抄控器默认源地址"],
                    sid=1)
    engine.expect_did("WRITE", "载波芯片注册信息0603", "** ** ** ** ** **", check_seq=False)


def set_gw_info():
    """
    设置网关PANID信息，模拟设备入网
    r"4aid+2panid+2pw+4gid+2sid"
    """
    config = engine.get_config()
    engine.send_local_msg("设置PANID", config["panid"])
    engine.expect_local_msg("确认")
    engine.wait(1)
    engine.send_did("WRITE", "载波芯片注册信息0603",
                    aid=config["测试设备地址"],
                    panid=config["panid"],
                    pw=config["设备PWD000A"],
                    device_gid=config["抄控器默认源地址"],
                    sid=8)
    engine.expect_did("WRITE", "载波芯片注册信息0603", "** ** ** ** ** **", check_seq=False)



