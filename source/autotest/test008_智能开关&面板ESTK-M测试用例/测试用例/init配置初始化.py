import engine
from autotest.公共用例.public00init配置初始化 import *


def init_设备信息识别():
    """
    04_设备信息识别
    1、识别设备类型：开关、面板
    2、识别按键数量：1、2、3、4
    3、根据设备信息区分设备类型和升级包等内容
    """
    def type_check_func(data):
        if len(data) == 2:
            config["被测设备类型"] = "面板"
        return True

    def num2_check_func(data):
        if len(data) == 6:
            config["被测设备按键数"] = 2
        return True

    def num3_check_func(data):
        if len(data) == 6:
            config["被测设备按键数"] = 3
        return True

    def num4_check_func(data):
        if len(data) == 6:
            config["被测设备按键数"] = 4
        return True

    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", type_check_func)

    engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道=2)
    engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",num2_check_func)
    engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道=3)
    engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",num3_check_func)
    engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道=4)
    engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",num4_check_func)

    if config["被测设备按键数"] == 1:
        if config["被测设备类型"] == "面板":
            engine.add_doc_info("\n\n******************************设备为1按键面板************************************\n\n")
        else:
            engine.add_doc_info("\n\n******************************设备为1按键开关************************************\n\n")
    if config["被测设备按键数"] == 2:
        if config["被测设备类型"] == "面板":
            engine.add_doc_info("\n\n******************************设备为2按键面板************************************\n\n")
        else:
            engine.add_doc_info("\n\n******************************设备为2按键开关************************************\n\n")
    if config["被测设备按键数"] == 3:
        engine.add_doc_info("\n\n******************************设备为3按键面板************************************\n\n")
    if config["被测设备按键数"] == 4:
        engine.add_doc_info("\n\n******************************设备为4按键面板************************************\n\n")

    if config["被测设备类型"] == "面板":
        config["设备描述信息设备制造商0003"] = r"ESTK-M(v2.0)-20210518"
        config["应用程序上一版发布版本"] = r"ESTK-M(v1.4)-20191205"  # 如果此处为空字符串时，表示不支持兼容性升级或手动测试。
        config["应用程序同版本号测试版本"] = r"ESTK-M(v2.0)-20210520"

    if config["被测设备类型"] == "开关" and config["被测设备按键数"] == 2:
        config["设备类型0001"] = "FF FF 02 00 22 01 02 00"
        config["设备描述信息设备制造商0003升级包"] = r"ESTK-M-2S5A(v2.0)-20210518"
        config["应用程序上一版发布版本升级包"] = r"ESTK-M-2S5A(v1.4)-20191205"  # 如果此处为空字符串时，表示不支持兼容性升级或手动测试。
        config["应用程序同版本号测试版本升级包"] = r"ESTK-M-2S5A(v2.0)-20210520"

    if config["被测设备类型"] == "面板" and config["被测设备按键数"] == 1:
        config["设备类型0001"] = "FF FF 02 00 00 01 01 00"
        config["设备描述信息设备制造商0003升级包"] = r"ESTK-01-M(v2.0)-20210518"
        config["应用程序上一版发布版本升级包"] = r"ESTK-01-M(v1.4)-20191205"  # 如果此处为空字符串时，表示不支持兼容性升级或手动测试。
        config["应用程序同版本号测试版本升级包"] = r"ESTK-01-M(v2.0)-20210520"


    if config["被测设备类型"] == "面板" and config["被测设备按键数"] == 2:
        config["设备类型0001"] = "FF FF 02 00 00 01 02 00"
        config["设备描述信息设备制造商0003升级包"] = r"ESTK-02-M(v2.0)-20210518"
        config["应用程序上一版发布版本升级包"] = r"ESTK-02-M(v1.4)-20191205"  # 如果此处为空字符串时，表示不支持兼容性升级或手动测试。
        config["应用程序同版本号测试版本升级包"] = r"ESTK-02-M(v2.0)-20210520"


    if config["被测设备类型"] == "面板" and config["被测设备按键数"] == 3:
        config["设备类型0001"] = "FF FF 02 00 00 01 03 00"
        config["设备描述信息设备制造商0003升级包"] = r"ESTK-03-M(v2.0)-20210518"
        config["应用程序上一版发布版本升级包"] = r"ESTK-03-M(v1.4)-20191205"  # 如果此处为空字符串时，表示不支持兼容性升级或手动测试。
        config["应用程序同版本号测试版本升级包"] = r"ESTK-03-M(v2.0)-20210520"


    if config["被测设备类型"] == "面板" and config["被测设备按键数"] == 4:
        config["设备类型0001"] = "FF FF 02 00 00 01 04 00"
        config["设备描述信息设备制造商0003升级包"] = r"ESTK-04-M(v2.0)-20210518"
        config["应用程序上一版发布版本升级包"] = r"ESTK-04-M(v1.4)-20191205"  # 如果此处为空字符串时，表示不支持兼容性升级或手动测试。
        config["应用程序同版本号测试版本升级包"] = r"ESTK-04-M(v2.0)-20210520"
