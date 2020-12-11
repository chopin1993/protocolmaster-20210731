import engine


def test_boardcast_single():
    """
    单个广播测试
    """
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.wait(3)
    engine.send_did("WRITE", "通断操作C012", "81", taid=0xffffffff, gids=[5,6,7],gid_type="U16")
    engine.wait(3)
    engine.send_did("WRITE", "通断操作C012", "01", taid=0xffffffff, gids=[5,6,7],gid_type="U8")
    engine.wait(3)
    engine.send_did("WRITE", "通断操作C012", "81", gids=[1,2,9],gid_type="BIT1")
    engine.wait(3)

def test_boardcat_mulit():
    """
    多个广播测试
    """
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.wait(3)
    engine.broadcast_send_multi_dids("WRITE",
                                     [1, 2, 3], "BIT1","通断操作C012", "81",
                                     [2, 3, 4], "U8", "通断操作C012", "81",
                                     [3, 4, 5], "U16", "通断操作C012", "81",
                                     )
    engine.wait(3)
    engine.broadcast_send_multi_dids("WRITE",
                                     [1, 2, 3], "BIT1","通断操作C012", "01",
                                     [2, 3, 4], "U8", "通断操作C012", "01",
                                     [3, 4, 5], "U16", "通断操作C012", "01",
                                     )


def test_crash_multi():
    """
    崩溃测试1
    """
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.wait(3)
    engine.send_multi_dids("WRITE", "通断操作C012", "81",
                                    "通断操作C012", "81",
                                     taid=0xffffffff,gid_type="BIT1")

def test_crash_signle():
    """
    崩溃测试-single
    """
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.wait(3)
    engine.send_did("WRITE", "通断操作C012", "81",taid=0xffffffff, gid_type="BIT1")