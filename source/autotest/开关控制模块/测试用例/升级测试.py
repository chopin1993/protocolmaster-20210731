# encoding:utf-8
import engine

测试组说明="升级方面测试"

def test_update():
    """
    测试程序功能
    1.升级前读取设备的版本信息
    2.升级
    3.升级之后读取设备版本号，确保升级成功
    """
    engine.send_did("READ", "设备描述信息设备制造商")
    engine.expect_did("READ", "设备描述信息设备制造商", "ESACT-1A(v1.4)-20171020")
    engine.update("升级文件")
    engine.send_did("READ", "设备描述信息设备制造商")
    engine.expect_did("READ", "设备描述信息设备制造商", "ESACT-1A(v1.4)-20171020")




