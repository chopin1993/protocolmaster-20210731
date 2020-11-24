import engine


def test_said_taid_string():
    """
    said taid
    """
    engine.send_did("READ", "0004",taid=464148)
    engine.expect_did("READ", "0004", "SSC1667-ADPT-V30B011",said=464148)


def test_said_taid_string2():
    """
    multi said taid
    """
    engine.send_multi_dids("READ", "0004","",
                                   "0004","",taid=464148)
    engine.expect_multi_dids("READ",
                                  "0004", "SSC1667-ADPT-V30B011",
                                  "0004", "SSC1667-ADPT-V30B011",
                                  said=464148)
