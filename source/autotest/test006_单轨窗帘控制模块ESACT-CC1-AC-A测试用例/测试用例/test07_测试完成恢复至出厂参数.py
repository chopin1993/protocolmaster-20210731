# encoding:utf-8
# 导入测试引擎

from autotest.公共用例.public常用测试模块 import *
from .常用测试模块 import *

测试组说明 = "测试完成恢复出厂参数"

config = engine.get_config()


def test_测试完成恢复出厂参数():
    """
    测试完成恢复出厂状态
    1、发送调试指令FF00，使设备恢复出厂设置
    此操作恢复出厂设置功能与设备本地按键恢复出厂设置功能相同，清除网关信息，继电器恢复默认状态，其他功能参数恢复至默认，
    硬件相关的参数或特殊应用参数不清除
    2、对所有的参数进行验证，保障调试指令正常
    """
    # 因为暂不支持FF00调试指令，所以通过抄控器设置panid=0，网关gid=1，模拟清除出厂信息。
    engine.add_doc_info('1、因为暂不支持FF00调试指令，所以通过抄控器设置panid=0，网关gid=1，模拟清除出厂信息。')
    panel00 = engine.create_role("清除密钥", 1)
    engine.send_local_msg("设置PANID", 0)
    engine.expect_local_msg("确认")
    engine.wait(5)
    panel00.send_did("WRITE", "载波芯片注册信息0603",
                     aid=config["测试设备地址"],
                     panid=0,
                     pw=config["设备PWD000A"],
                     device_gid=panel00.said,
                     sid=1)
    panel00.expect_did("WRITE", "载波芯片注册信息0603", "** ** ** ** ** **", check_seq=False)
    engine.wait(15, '预留15s间隔')
    return_to_factory()

    engine.add_doc_info('2、恢复出厂默认参数并进行验证，便于后续的测试项目运行')
    read_default_configuration()
    engine.wait(10, tips='恢复至出厂参数成功')
