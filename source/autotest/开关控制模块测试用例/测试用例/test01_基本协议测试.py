# encoding:utf-8
import engine

测试组说明 = "基本协议类报文测试"


# def test_设置密钥():
#     """设置网关的PANID"""
#     config = engine.get_config()
#     engine.send_local_msg("设置PANID", config["panid"])
#     engine.expect_local_msg("确认")
def test_设备类型0001():
    """设备类型0001"""
    engine.send_did("READ", "设备类型0001")
    engine.expect_did("READ", "设备类型0001", config["设备类型0001"])


def test_应用层通讯协议及版本0002():
    """应用层通讯协议及版本0002"""
    engine.send_did("READ", "应用层通讯协议及版本0002")
    engine.expect_did("READ", "应用层通讯协议及版本0002", config["应用层通讯协议及版本0002"])


def test_设备描述信息设备制造商0003():
    """设备描述信息设备制造商0003"""
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"])


def test_载波版本号0004():
    """
    载波版本号0004
    每次测试按照载波的最新版本进行测试
    """
    engine.send_did("READ", "载波版本号0004")
    engine.expect_did("READ", "载波版本号0004", config["载波版本号0004"])


def test_适配层版本号0606():
    """适配层版本号0606
    每次测试按照载波的最新版本进行测试"""
    engine.send_did("READ", "适配层版本号0606")
    engine.expect_did("READ", "适配层版本号0606", config["适配层版本号0606"])


def test_网络层版本号060A():
    """网络层版本号060A
    每次测试按照载波的最新版本进行测试"""
    engine.send_did("READ", "网络层版本号060A")
    engine.expect_did("READ", "网络层版本号060A", config["网络层版本号060A"])


def test_DKEY0005():
    """DKEY0005"""
    engine.send_did("READ", "DKEY0005")
    engine.expect_did("READ", "DKEY0005", config["DKEY0005"])


def test_SN0007():
    """SN0007"""
    engine.send_did("READ", "SN0007")
    engine.expect_did("READ", "SN0007", config["SN0007"])


def test_设备PWD000A():
    """设备PWD000A"""
    engine.send_did("READ", "设备PWD000A")
    engine.expect_did("READ", "设备PWD000A", config["设备PWD000A"])


def test_组合报文():
    """
    多DID组合报文测试
    1、组合报文查询：设备类型0001、设备描述信息设备制造商0003、DKEY0005、SN0007
    2、组合报文查询：适配层物料编码0602、适配层版本号0606、网络层物料编码0609、网络层版本号060A
    """
    engine.send_multi_dids("READ", "设备类型0001", "",
                           "设备描述信息设备制造商0003", "",
                           "DKEY0005", "",
                           "SN0007", "")
    engine.expect_multi_dids("READ", "设备类型0001", config["设备类型0001"],
                             "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"],
                             "DKEY0005", config["DKEY0005"],
                             "SN0007", config["SN0007"])

    engine.send_multi_dids("READ", "适配层物料编码0602", "",
                           "适配层版本号0606", "",
                           "网络层物料编码0609", "",
                           "网络层版本号060A", "")
    engine.expect_multi_dids("READ", "适配层物料编码0602", config["适配层物料编码0602"],
                             "适配层版本号0606", config["适配层版本号0606"],
                             "网络层物料编码0609", config["网络层物料编码0609"],
                             "网络层版本号060A", config["网络层版本号060A"])


config = engine.get_config()
