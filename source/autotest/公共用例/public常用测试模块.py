# encoding:utf-8
# 导入测试引擎
import engine
import time
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
    engine.wait(5)
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
    engine.wait(5)
    engine.send_did("WRITE", "载波芯片注册信息0603",
                    aid=aid,
                    panid=panid,
                    pw=pw,
                    device_gid=device_gid,
                    sid=sid,
                    taid=aid)
    engine.expect_did("WRITE", "载波芯片注册信息0603", "** ** ** ** ** **", check_seq=False, said=aid)


def power_control(init_time=config["被测设备上电后初始化时间"]):
    """
    测试工装控制通断电
    通过控制工装通断，实现给测试设备的通断电，实现断电测试场景
    passed_time 断电重启后设备用时
    """
    from autotest.公共用例.public00init配置初始化 import init_触发设备检测监测器

    engine.add_doc_info("测试工装控制通断电")
    engine.wait(seconds=1, tips='保证和之前的测试存在1s间隔')
    engine.control_relay(0, 0)
    engine.wait(seconds=10, tips='保证被测设备充分断电')
    engine.control_relay(0, 1)

    start_time = time.time()
    engine.wait(seconds=init_time)  # 普通载波设备上电初始化，预留足够时间供载波初始化
    init_触发设备检测监测器()
    passed_time = time.time() - start_time
    engine.add_doc_info('载波设备上电初始化+触发设备检测监测器共计用时{:.3f}秒'.format(passed_time))

    return passed_time
