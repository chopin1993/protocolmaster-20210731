import engine


def test_multi_dids():
    "多DID测试"
    engine.send_multi_dids("READ", "DKEY", "", "SN", "", "设备类型", "")
    engine.expect_multi_dids("READ",
                             "DKEY", "** ** ** ** ** ** ** **",
                             "SN", "** ** ** ** ** ** ** ** ** ** ** **",
                             "设备类型", "** ** ** ** ** ** ** **",
                             timeout=3)
