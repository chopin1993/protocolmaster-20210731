import engine
from autotest.公共用例.public00init配置初始化 import *


def init_clear_gw():
    "清除设备网关信息"
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
    engine.wait(1)
