import engine
from engine.spy_device import SpyDevice

config = engine.get_config()


def init_配置初始化():
    "01_设置aid、波特率和透传"
    engine.create_role("monitor", config["抄控器默认源地址"])
    engine.send_local_msg("设置透传模式", 1)
    engine.expect_local_msg("确认")


def init_配置设备初始供电():
    """
    02_配置设备初始供电
    默认打开通道0，给被测设备供电
    """
    engine.control_relay(0, 0)
    engine.wait(5, tips='给被测设备断电，断电5s')
    engine.control_relay(0, 1)
    engine.wait(config["被测设备上电后初始化时间"],
                tips='给被测设备供电，等待被测设备上电后初始化时间{}s'.format(config["被测设备上电后初始化时间"]))


def init_触发设备检测监测器():
    """
    03_触发设备检测监测器
    """

    # 检测swb_bus接口
    engine.reset_swb_bus(0)

    def validate_func(data):
        if len(data) == 2:
            engine.add_doc_info("\n\n***************监测器探测失败,测试过"
                                "程中将忽略和监测器相关的判断!!!!!!!!!!!!!!!!!!!!!!!!!***\n\n")
        return True

    SpyDevice.instance().clear_status()
    engine.send_did("WRITE", "自动测试FC00", 密码=config["设备PWD000A"], 自动测试命令="触发SWB总线探测")
    engine.expect_did("WRITE", "自动测试FC00", validate_func)
