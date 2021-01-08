# encoding:utf-8
# 导入测试引擎
import engine

config = engine.get_config()


def clear_gw_info(aid=config["测试设备地址"], pw=config["设备PWD000A"]):
    """
    清除网关PANID信息，模拟出厂设备
    r"4aid+2panid+2pw+4gid+2sid"
    :param aid:
    :param pw:
    """
    engine.send_local_msg("设置PANID", 0)
    engine.expect_local_msg("确认")
    engine.wait(1)
    engine.send_did("WRITE", "载波芯片注册信息0603",
                    aid=aid,
                    panid=0,
                    pw=pw,
                    device_gid=config["抄控器默认源地址"],
                    sid=1,
                    taid=aid)
    engine.expect_did("WRITE", "载波芯片注册信息0603", "** ** ** ** ** **", check_seq=False, said=aid)


def set_gw_info(aid=config["测试设备地址"],
                panid=config["panid"],
                pw=config["设备PWD000A"],
                device_gid=config["抄控器默认源地址"],
                sid=8):
    """
    设置网关PANID信息，模拟设备入网
    r"4aid+2panid+2pw+4gid+2sid"
    """
    engine.send_local_msg("设置PANID", panid)
    engine.expect_local_msg("确认")
    engine.wait(1)
    engine.send_did("WRITE", "载波芯片注册信息0603",
                    aid=aid,
                    panid=panid,
                    pw=pw,
                    device_gid=device_gid,
                    sid=sid,
                    taid=aid)
    engine.expect_did("WRITE", "载波芯片注册信息0603", "** ** ** ** ** **", check_seq=False, said=aid)


def power_control(time=config["被测设备上电后初始化时间"]):
    """
    测试工装控制通断电
    通过控制工装通断，实现给测试设备的通断电，实现断电测试场景
    """
    engine.add_doc_info("测试工装控制通断电")
    engine.wait(seconds=2,tips='保证和之前的测试存在2s间隔')
    engine.control_relay(channel=0,value=0)
    engine.wait(seconds=10,tips='保证被测设备充分断电')
    # config = engine.get_config()
    # engine.send_did("WRITE", "通断操作C012", "01", taid=config["前置通断电工装AID"])
    # engine.expect_did("WRITE", "通断操作C012", "00", said=config["前置通断电工装AID"])
    # engine.wait(seconds=5)  # 充分断电
    # engine.send_did("WRITE", "通断操作C012", "81", taid=config["前置通断电工装AID"])
    # engine.expect_did("WRITE", "通断操作C012", "01", said=config["前置通断电工装AID"])
    if time != 0:
        engine.wait(seconds=time)  # 普通载波设备上电初始化时间约10s，预留足够时间供载波初始化
