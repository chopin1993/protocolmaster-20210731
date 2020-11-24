import engine


def test_multi_dids():
    "多DID测试"
    engine.send_multi_dids("READ", "DKEY0005", "", "SN0007", "", "SN0007", "")
    engine.expect_multi_dids("READ",
                             "DKEY0005", "** ** ** ** ** ** ** **",
                             "SN0007", "** ** ** ** ** ** ** ** ** ** ** **",
                             "SN0007", "** ** ** ** ** ** ** ** ** ** ** **",
                             timeout=3)
