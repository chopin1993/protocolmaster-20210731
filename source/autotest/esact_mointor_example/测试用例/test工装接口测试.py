import engine

def test_input():
    """
    输入测试-int
    """
    engine.set_device_input("按键输入", 1)
    engine.wait(5)



def test_input2():
    """
    输入测试-hexstr
    """
    engine.set_device_input("按键输入", "02")
    engine.wait(5)


