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
    engine.report_check_enable_all(True)
    # 因为暂不支持FF00调试指令，所以通过抄控器设置panid=0，网关gid=1，模拟清除出厂信息。
    engine.add_doc_info('1、因为暂不支持FF00调试指令，所以通过抄控器设置panid=0，网关gid=1，模拟清除出厂信息。')
    clear_gw_info()
    engine.wait((15 - 1), allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "读传感器数据B701", '09 **',
                             "读传感器数据B701", '0B ** **', ack=True)
    engine.report_check_enable_all(False)
    # engine.add_doc_info("发送调试指令，所有的状态和配置参数恢复至出厂参数")
    # engine.send_did("WRITE", "自动测试FC00", 密码=config["设备PWD000A"], 自动测试命令="清除系统所有信息")
    # engine.expect_did("WRITE", "自动测试FC00", 密码=config["设备PWD000A"], 自动测试命令="清除系统所有信息")
    # engine.wait(10, tips='预留10s时间供设备清除系统所有信息')
    #
    # engine.add_doc_info('将自动测试FC00不能清除的关键参数，恢复至出厂默认参数')

    engine.add_doc_info('2、恢复出厂默认参数并进行验证，便于后续的测试项目运行')
    return_to_factory()

    engine.add_doc_info('3、再次断电重启，查看恢复出厂后的参数仍然正常；')
    power_control()
    read_default_configuration()
    engine.wait(120,tips='恢复至出厂参数成功')