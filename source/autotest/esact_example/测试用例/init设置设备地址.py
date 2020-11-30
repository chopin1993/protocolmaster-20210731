import engine


def test_1():
    "打开通用配置"
    config = engine.get_config()
    engine.send_local_msg("设置透传模式", 1)
    engine.expect_local_msg("确认")
