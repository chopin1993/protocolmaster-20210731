import engine

def init_配置初始化():
    "配置初始化"
    config = engine.get_config()
    engine.setting_uart(0, config["波特率"], config['校验位'])
    engine.create_role("monitor", config["抄控器默认源地址"])
    engine.send_local_msg("设置透传模式", 1)
    engine.expect_local_msg("确认")
