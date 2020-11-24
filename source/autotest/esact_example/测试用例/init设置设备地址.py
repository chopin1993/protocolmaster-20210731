import engine


def test_1():
    "设置panid"
    config = engine.get_config()
    engine.send_local_msg("设置PANID", config["panid"])
    engine.expect_local_msg("确认")
