import engine
from autotest.公共用例.public00init配置初始化 import *

def init_设备硬件版本识别():
    """
    04_设备硬件版本识别
    """
    def type_check_func(data):
        if len(data) == 2:
            config["被测设备硬件版本"] = "可控硅版本"

        return True

    engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
    engine.expect_did("READ", "继电器过零点动作延迟时间C020", type_check_func)
    if config["被测设备硬件版本"] == "可控硅版本":
        engine.add_doc_info("\n\n******************************设备硬件版本为可控硅版本******************************\n\n")
    else:
        engine.add_doc_info("\n\n******************************设备硬件版本为继电器版本******************************\n\n")