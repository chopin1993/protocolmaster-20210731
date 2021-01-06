import engine
from engine.spy_device import SpyDevice
config = engine.get_config()

def init_配置初始化():
    "配置初始化"
    engine.setting_uart(0, config["波特率"], config['校验位'])
    engine.create_role("monitor", config["抄控器默认源地址"])
    engine.send_local_msg("设置透传模式", 1)
    engine.expect_local_msg("确认")


def init_触发设备检测监测器():
    """
    触发设备检测监测器
    """
    def validate_func(data):
        if len(data) == 2:
            engine.add_doc_info("\n\n***************监测器探测失败,测试过"
                                "程中将忽略和监测器相关的判断!!!!!!!!!!!!!!!!!!!!!!!!!***\n\n")
        return True

    SpyDevice.instance().clear_status()
    engine.send_did("WRITE", "自动测试FC00", 密码=config["设备PWD000A"], 自动测试命令="触发SWB总线探测")
    engine.expect_did("WRITE", "自动测试FC00", validate_func)

    engine.reset_swb_bus(0)