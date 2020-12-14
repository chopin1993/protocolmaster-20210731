# encoding:utf-8
import engine

测试组说明="升级方面测试"

def assert_version_adaptor(version):
    engine.send_did("READ", "0606")
    engine.expect_did("READ", "0606", version)

def assert_version_network(version):
    engine.send_did("READ", "060a")
    engine.expect_did("READ", "0606", version)


def test_update1():
    """
    升级适配层
    """
    engine.update("ESMD-AD63(v2.1)-20170210-update.bin")









