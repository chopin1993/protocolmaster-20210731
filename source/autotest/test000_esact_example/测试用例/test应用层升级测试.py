# encoding:utf-8
import engine

测试组说明="升级方面测试"

def assert_version1():
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003",  "ESACT-1A(v1.5)-20200805")

def assert_version2():
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003",  "ESACT-1A(v1.5)-20200808")

def test_update1():
    """
    升级ESACT-1S1A(v1.5)-20200805
    """
    engine.update("ESACT-1A(v1.5)-20200805.bin")
    engine.wait(30)
    assert_version1()


def test_update2():
    """
    升级ESACT-1S1A(v1.5)-20200808
    """
    assert_version1()
    engine.update("ESACT-1A(v1.5)-20200808.bin")
    engine.wait(30)
    assert_version2()

def test_break_continue():
    """
    断点续传
    发送到100包之后，停止发送，设备重发三次之后，会停止升级。再启动发送，设备会继续请求101包。
    发送数据不对时，设备校验不过，会升级失败。
    """
    assert_version2()
    def controller_fun(seq):
        if seq < 10:
            return seq
        else:
            return None
    engine.update("ESACT-1A(v1.5)-20200805.bin",controller_fun, )
    engine.wait(3)

    # 读版本号

    def controller_fun2(seq):
        if seq < 10:
            engine.add_fail_test("没有断点续传")
        else:
           return seq
    engine.update("ESACT-1A(v1.5)-20200805.bin",controller_fun2)

    engine.wait(30)
    assert_version1()



def test_pwoeroff_start():
    """
    断电重传
    1.升级前读取设备的版本信息
    2.升级
    3.升级之后读取设备版本号，确保升级成功
    """
    assert_version1()
    def controller_fun(seq):
        if seq < 10:
            return seq
        elif seq == 0xffff:
            return seq
        else:
            return None
    engine.update("ESACT-1A(v1.5)-20200808.bin",controller_fun)

    engine.wait(20,tips="请给设备断电")
    # 断电
    reqs = engine.update("ESACT-1A(v1.5)-20200808.bin")

    if reqs[0] != 1:
        engine.add_fail_test("断电重传失败")
    engine.wait(30, tips="设备升级完成，校验版本")
    assert_version2()

def test_update_control():
    "升级+控制"
    def device_ctrl(second):
        if second == 3:
            engine.wait(3)
            for i in range(10):
                if i %2 == 0:
                    engine.send_did("WRITE", "通断操作C012", "81")
                    engine.expect_did("WRITE", "通断操作C012", "01", timeout=9)
                    engine.wait(3)
                else:
                    engine.send_did("WRITE", "通断操作C012", "01")
                    engine.expect_did("WRITE", "通断操作C012", "00", timeout=9)
                    engine.wait(3)

    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01", timeout=9)
    engine.wait(3)
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00", timeout=9)

    assert_version2()
    engine.update("ESACT-1A(v1.5)-20200805.bin", None, device_ctrl)
    engine.wait(40, tips="设备升级完成，校验版本")
    assert_version1()
