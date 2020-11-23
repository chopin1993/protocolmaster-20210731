import engine


def test_r_string():
    """
    原始报文读取sn
    """
    engine.send_raw("02 07 00 00")
    engine.expect_raw("02 07 00 0C 32 01 10 10 00 51 80 32 01 00 00 16")


def test_r_string2():
    """
    原始报文读取sn2**
    """
    engine.send_raw("02 07 00 00")
    engine.expect_raw("02 07 00 0C 32 01 10 10 00 51 80 32 01 00 ** **")