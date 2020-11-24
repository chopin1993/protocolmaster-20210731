import engine


def test_r_string():
    """
    单个广播测试
    """
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.wait(3)
    engine.send_did("WRITE", "通断操作C012", "81", taid=0xffffffff, gids=[0,1,2],gid_type="U16")
    engine.wait(3)
    engine.send_did("WRITE", "通断操作C012", "01", taid=0xffffffff, gids=[0,1,2],gid_type="U8")
    engine.wait(3)
    engine.send_did("WRITE", "通断操作C012", "81", taid=0xffffffff, gids=[0,1,2],gid_type="BIT1")
    engine.wait(3)

def test_r_string2():
    """
    多个广播测试
    """
    engine.send_raw("02 07 00 00")
    engine.expect_raw("02 07 00 0C 32 01 10 10 00 51 80 32 01 00 ** **")