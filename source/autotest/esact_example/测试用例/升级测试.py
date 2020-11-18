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
    engine.update("ESACT-1S1A(v1.5)-20200805.bin")
    engine.send_did("READ", "设备描述信息设备制造商")
    engine.expect_did("READ", "设备描述信息设备制造商", "ESACT-1A(v1.4)-20171020")

def test_break_continue():
    """
    断点续传
    发送到100包之后，停止发送，设备重发三次之后，会停止升级。再启动发送，设备会继续请求101包。
    发送数据不对时，设备校验不过，会升级失败。
    """
    def controller_fun(seq):
        if seq < 100:
            return seq
        else:
            return None

    engine.send_did("READ", "设备描述信息设备制造商")
    expect_seq = [1]*100
    expect_seq.append(3)
    engine.expect_did("READ", "设备描述信息设备制造商", "ESACT-1A(v1.4)-20171020")
    engine.update("ESACT-1S1A(v1.5)-20200805.bin", controller_fun, expect_seq)

    expect_seq = [0]*100
    expect_seq.extend([1]*1000)
    engine.update("ESACT-1S1A(v1.5)-20200805.bin", None, expect_seq)
    engine.send_did("READ", "设备描述信息设备制造商")
    engine.expect_did("READ", "设备描述信息设备制造商", "ESACT-1A(v1.4)-20171020")


def update_fail():
    """
    升级crc校验失败
    """
    #engine.



