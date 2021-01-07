import engine

def test_non_exist_did():
    """
    失败测试-不存在的did
    """
    engine.send_did("WRITE", "主动上报使能标",  传感器类型=0, 上报命令=0)
