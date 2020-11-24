import engine

def test_wait1():
    """
    等待时间测试
    """
    engine.send_did("WRITE", "主动上报使能标志D005",  传感器类型=0, 上报命令=0)
    engine.wait(3, allowed_message=False)


def test_wait2():
    """
    等待时间测试2
    """
    engine.send_did("WRITE", "主动上报使能标志D005",  传感器类型=0, 上报命令=0)
    engine.wait(3, allowed_message=True)


def test_user():
    """
    手动测试失败
    """
    engine.add_fail_test("手动测试失败")
