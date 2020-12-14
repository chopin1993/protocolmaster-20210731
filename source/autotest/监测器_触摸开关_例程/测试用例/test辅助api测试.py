import engine

def test_wait1():
    """
    失败测试-等待时间测试
    """
    engine.send_did("WRITE", "主动上报使能标志D005",  传感器类型=0, 上报命令=0)
    engine.wait(3, allowed_message=False)


def test_wait2():
    """
    等待时间测试
    """
    engine.send_did("WRITE", "主动上报使能标志D005",  传感器类型=0, 上报命令=0)
    engine.wait(3, allowed_message=True)


def test_wait3():
    """
    第三者回复
    """
    engine.send_did("READ", "0003", "", taid=464148)
    engine.wait(3, allowed_message=False)

def test_wait4():
    """
    失败测试_第三者回复
    """
    engine.send_did("READ", "0003", "", taid=464148)
    engine.wait(3, allowed_message=False, said=464148)

def test_user():
    """
    失败测试-手动期望失败
    """
    engine.add_fail_test("手动测试失败")
