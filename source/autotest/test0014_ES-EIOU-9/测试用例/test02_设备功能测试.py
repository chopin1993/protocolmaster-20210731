# encoding:utf-8
# 导入测试引擎
# from autotest.公共用例.public05远程升级测试 import *
import engine
from .常用测试模块 import *

测试组说明 = "设备功能测试"


def test_实验():
    """
    134_实验
    """
    engine.send_FE02_did("READ", "IO配置D201", "01")
    engine.expect_FE02_did("READ", "IO配置D201", "01 00")

    # engine.send_did("WRITE", "22V通断电FE04", "01 20")
    # engine.expect_did("WRITE", "22V通断电FE04", "01 20")


def test_模式与数据测试():
    """
    11_模式与数据测试D201
    1.BIOU-9支持各IO模式配置、读取，输入、输出的数据可读取；
    2。模式读写数据标识为D201，读取时携带通道1-9，携带00表示读取全部通道，设备返回为通道+类型组合；
    3.数字输入模式：配置通道1为数字输入模式，UIO1与GND未短接时两数据标识返回均为00，UIO1与GND短接时两数据标识返回均为01；数字量数据返回格式为 通道+类型+数据类型01+数据，此时数据为1Byte；
    4.数字输出模式：配置通道1为数字输出模式，设置输出数据为01表示UIO1与GND短接，输出数据00表示UIO1与GND未短接。设置和读取数据格式为 通道+类型+数据类型01+数据，此时数据为1Byte；
    5.模拟输入模式：配置通道5为NTC10K-3435，模拟输入读取返回数据格式为 通道+类型+数据类型02+数据，此时数据为4Byte（D200）或5Byte(FFA2)；
    """

    engine.add_doc_info("1、模式读写")
    # for i in range (1,9):
    #     engine.send_FE02_did("READ", "IO配置D201", "0i")
    #     engine.expect_FE02_did("READ", "IO配置D201", "ji FF")
    # else:
    #     return 0
    engine.send_FE02_did("READ", "IO配置D201", "01 02 05 09")
    engine.expect_FE02_did("READ", "IO配置D201", "01 FF 02 FF 05 FF 09 FF")
    engine.send_FE02_did("READ", "IO配置D201", "00")
    engine.expect_FE02_did("READ", "IO配置D201", "01 FF 02 FF 03 FF 04 FF 05 FF  06 FF 07 FF  08 FF 09 FF")

    # engine.send_FE02_did("READ", "IO配置D201", "01")
    # engine.expect_FE02_did("READ", "IO配置D201", "01 FF")
    # engine.send_FE02_did("READ", "IO配置D201", "02")
    # engine.expect_FE02_did("READ", "IO配置D201", "02 FF")
    # engine.send_FE02_did("READ", "IO配置D201", "03")
    # engine.expect_FE02_did("READ", "IO配置D201", "03 FF")
    # engine.send_FE02_did("READ", "IO配置D201", "04")
    # engine.expect_FE02_did("READ", "IO配置D201", "04 FF")
    # engine.send_FE02_did("READ", "IO配置D201", "05")
    # engine.expect_FE02_did("READ", "IO配置D201", "05 FF")
    # engine.send_FE02_did("READ", "IO配置D201", "06")
    # engine.expect_FE02_did("READ", "IO配置D201", "06 FF")
    # engine.send_FE02_did("READ", "IO配置D201", "07")
    # engine.expect_FE02_did("READ", "IO配置D201", "07 FF")
    # engine.send_FE02_did("READ", "IO配置D201", "08")
    # engine.expect_FE02_did("READ", "IO配置D201", "08 FF")
    # engine.send_FE02_did("READ", "IO配置D201", "09")
    # engine.expect_FE02_did("READ", "IO配置D201", "09 FF")

    engine.send_FE02_did("READ", "IO配置D201", "")
    engine.expect_FE02_did("READ", "IO配置D201", "03 00")
    engine.send_FE02_did("READ", "IO配置D201", "0A")
    engine.expect_FE02_did("READ", "IO配置D201", "03 00")
    engine.send_FE02_did("READ", "IO配置D201", "00 01 0A")
    engine.expect_FE02_did("READ", "IO配置D201", "03 00")
    engine.send_FE02_did("READ", "IO配置D201", "01 06 0A")
    engine.expect_FE02_did("READ", "IO配置D201", "03 00")

    engine.send_FE02_did("WRITE", "IO配置D201", "01 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "01 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "02 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "02 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "03 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "03 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "04 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "04 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "05 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "05 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "06 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "06 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "07 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "07 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "08 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "08 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "09 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "09 00")

    engine.send_FE02_did("READ", "IO配置D201", "01")
    engine.expect_FE02_did("READ", "IO配置D201", "01 00")
    engine.send_FE02_did("READ", "IO配置D201", "02")
    engine.expect_FE02_did("READ", "IO配置D201", "02 00")
    engine.send_FE02_did("READ", "IO配置D201", "03")
    engine.expect_FE02_did("READ", "IO配置D201", "03 00")
    engine.send_FE02_did("READ", "IO配置D201", "04")
    engine.expect_FE02_did("READ", "IO配置D201", "04 00")
    engine.send_FE02_did("READ", "IO配置D201", "05")
    engine.expect_FE02_did("READ", "IO配置D201", "05 00")
    engine.send_FE02_did("READ", "IO配置D201", "06")
    engine.expect_FE02_did("READ", "IO配置D201", "06 00")
    engine.send_FE02_did("READ", "IO配置D201", "07")
    engine.expect_FE02_did("READ", "IO配置D201", "07 00")
    engine.send_FE02_did("READ", "IO配置D201", "08")
    engine.expect_FE02_did("READ", "IO配置D201", "08 00")
    engine.send_FE02_did("READ", "IO配置D201", "09")
    engine.expect_FE02_did("READ", "IO配置D201", "09 00")

    engine.send_FE02_did("WRITE", "IO配置D201", "00 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "03 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "01 04")
    engine.expect_FE02_did("WRITE", "IO配置D201", "03 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "01 09")
    engine.expect_FE02_did("WRITE", "IO配置D201", "03 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "01 19")
    engine.expect_FE02_did("WRITE", "IO配置D201", "03 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "01 26")
    engine.expect_FE02_did("WRITE", "IO配置D201", "03 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "01 00 09 09")
    engine.expect_FE02_did("WRITE", "IO配置D201", "03 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "01 01 0A 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "03 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "01 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "01 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "01 00 02 00 03 00 04 00 05 00 06 00 07 00 08 00 09 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "01 00 02 00 03 00 04 00 05 00 06 00 07 00 08 00 09 00")
    engine.send_FE02_did("READ", "IO配置D201", "01 00")
    engine.expect_FE02_did("READ", "IO配置D201", "01 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "01 00 02 00 03 00 04 00 05 00 06 00 07 00 08 00 09 00")
    engine.send_FE02_did("READ", "IO配置D201", "00")
    engine.expect_FE02_did("READ", "IO配置D201", "01 FF 02 FF 03 FF 04 FF 05 FF 06 FF 07 FF 08 FF 09 FF")

    engine.send_FE02_did("READ", "IO配置D201", "00 00")
    engine.expect_FE02_did("READ", "IO配置D201", "03 00")
    engine.send_FE02_did("READ", "IO配置D201", "01 04")
    engine.expect_FE02_did("READ", "IO配置D201", "03 00")
    engine.send_FE02_did("READ", "IO配置D201", "01 09")
    engine.expect_FE02_did("READ", "IO配置D201", "03 00")
    engine.send_FE02_did("READ", "IO配置D201", "01 19")
    engine.expect_FE02_did("READ", "IO配置D201", "03 00")
    engine.send_FE02_did("READ", "IO配置D201", "01 26")
    engine.expect_FE02_did("READ", "IO配置D201", "03 00")
    engine.send_FE02_did("READ", "IO配置D201", "00 09 09")
    engine.expect_FE02_did("READ", "IO配置D201", "03 00")
    engine.send_FE02_did("READ", "IO配置D201", "01 0A 00")
    engine.expect_FE02_did("READ", "IO配置D201", "03 00")
    engine.send_FE02_did("READ", "IO配置D201", "00")
    engine.expect_FE02_did("READ", "IO配置D201", "01 FF 02 FF 03 FF 04 FF 05 FF 06 FF 07 FF 08 FF 09 FF")

    engine.add_doc_info("2、数据读写")
    # 数字输入模式
    engine.send_FE02_did("READ", "IO配置D201", "00")
    engine.expect_FE02_did("READ", "IO配置D201", "01 FF 02 FF 03 FF 04 FF 05 FF 06 FF 07 FF 08 FF 09 FF")
    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 FF 01 00 02 FF 01 00 03 FF 01 00 04 FF 01 00 05 FF 01 00 06 FF 01 00 07 FF 01 00 08 FF 01 00 09 FF 01 00")
    engine.send_FE02_did("WRITE", "IO操作D200", "01 FF 01 01 02 FF 01 01")
    engine.expect_FE02_did("WRITE", "IO操作D200", "03 00")
    engine.send_FE02_did("WRITE", "IO操作D200", "08 FF 01 01 09 FF 01 01")
    engine.expect_FE02_did("WRITE", "IO操作D200", "03 00")

    engine.send_FE02_did("WRITE", "IO配置D201", "01 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "01 00")
    engine.send_FE02_did("READ", "IO配置D201", "01")
    engine.expect_FE02_did("READ", "IO配置D201", "01 00")
    engine.send_FE02_did("READ", "IO操作D200", "01")
    engine.expect_FE02_did("READ", "IO操作D200", "01 00 01 00")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "01")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2", "01 00 01 00")

    # UI01如何和GND短接;先打开继电器第26路，即开启UI与GND短接
    engine.add_doc_FE02_info("UI01如何和GND短接")
    engine.send_did("WRITE", "22V通断电FE04", "01 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1A")
    engine.send_FE02_did("WRITE", "IO配置D201", "01 01 01 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "01 01 01 00")
    engine.send_FE02_did("READ", "IO操作D200", "01")
    engine.expect_FE02_did("READ", "IO操作D200", "01 00 01 01")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "01")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2", "01 00 01 01")
    engine.send_did("WRITE", "22V通断电FE04", "00 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1A")

    # 数字输出模式UI01
    engine.send_FE02_did("WRITE", "IO配置D201", "01 01")
    engine.expect_FE02_did("WRITE", "IO配置D201", "01 01")
    engine.send_FE02_did("READ", "IO配置D201", "01")
    engine.expect_FE02_did("READ", "IO配置D201", "01 01")
    engine.send_FE02_did("WRITE", "IO操作D200", "01 01 01 01")
    engine.expect_FE02_did("WRITE", "IO操作D200", "01 01 01 01")
    engine.send_FE02_did("READ", "IO操作D200", "01")
    engine.expect_FE02_did("READ", "IO操作D200", "01 01 01 01")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "01")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2", "01 01 01 01")
    engine.send_FE02_did("WRITE", "IO操作D200", "01 01 01 00")
    engine.expect_FE02_did("WRITE", "IO操作D200", "01 01 01 00")
    engine.send_FE02_did("READ", "IO操作D200", "01")
    engine.expect_FE02_did("READ", "IO操作D200", "01 01 01 00")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "01")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2", "01 00 01 00")

    # 设置UI05通道为NTC10K-3435，使用万用表测量电阻值**KΩ（未完）
    engine.send_FE02_did("WRITE", "IO配置D201", "05 20")
    engine.expect_FE02_did("WRITE", "IO配置D201", "05 20")
    engine.send_FE02_did("READ", "IO配置D201", "05")
    engine.expect_FE02_did("READ", "IO配置D201", "05 20")
    engine.send_FE02_did("READ", "IO操作D200", "05")
    engine.expect_FE02_did("READ", "IO操作D200", "05 20 02 ** ** ** **")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "05")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2", "05 20 02 ** ** ** ** **")
    # 设备电阻值,做差
    # Evalue=data


def test_数字输入模拟测试():
    """
    12_模式与数据测试D200
     """
    # 设置所有通道均为数字输入模式
    # for i in range(1, 9):
    #     engine.send_FE02_did("WRITE", "IO配置D201", "0i 00")
    #     engine.expect_FE02_did("WRITE", "IO配置D201", "0i 00")
    # else:
    #     return 0
    engine.send_FE02_did("WRITE", "IO配置D201", "01 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "01 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "02 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "02 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "03 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "03 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "04 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "04 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "05 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "05 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "06 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "06 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "07 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "07 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "08 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "08 00")
    engine.send_FE02_did("WRITE", "IO配置D201", "09 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "09 00")
    engine.send_FE02_did("READ", "IO配置D201", "00")
    engine.expect_FE02_did("READ", "IO配置D201", "01 00 02 00 03 00 04 00 05 00 06 00 07 00 08 00 09 00")

    # 断电后重新读取模式
    engine.send_did("WRITE", "22V通断电FE04", "00 20")
    engine.expect_did("WRITE", "22V通断电FE04", "00 20")
    engine.wait(5, allowed_message=True)
    engine.send_did("WRITE", "22V通断电FE04", "01 20")
    engine.expect_did("WRITE", "22V通断电FE04", "01 20")
    engine.wait(125, allowed_message=True)
    engine.send_FE02_did("READ", "IO配置D201", "00")
    engine.expect_FE02_did("READ", "IO配置D201", "01 00 02 00 03 00 04 00 05 00 06 00 07 00 08 00 09 00")

    # 输入模式下设置通道数据，设备回复错误
    engine.send_FE02_did("WRITE", "IO操作D200", "01 00 01 00")
    engine.expect_FE02_did("WRITE", "IO操作D200", "03 00")
    engine.send_FE02_did("WRITE", "IO操作D200",
                         "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")
    engine.expect_FE02_did("WRITE", "IO操作D200", "03 00")
    engine.send_FE02_did("WRITE", "IO操作D200",
                         "01 01 01 00 02 01 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")
    engine.expect_FE02_did("WRITE", "IO操作D200", "03 00")

    # 使用工具将UIO与GND短接，测试读取数据是否根据短接情况变化；(未完)
    engine.send_FE02_did("WRITE", "IO配置D201", "01 00 02 00 03 00 04 00 05 00 06 00 07 00 08 00 09 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "01 00 02 00 03 00 04 00 05 00 06 00 07 00 08 00 09 00")
    # 通道1
    engine.send_did("WRITE", "22V通断电FE04", "01 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1A")
    engine.send_FE02_did("WRITE", "IO配置D201",
                         "01 00 01 01 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")
    engine.expect_FE02_did("WRITE", "IO配置D201",
                           "01 00 01 01 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")
    engine.send_did("WRITE", "22V通断电FE04", "00 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1A")
    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")

    # 通道2
    engine.send_did("WRITE", "22V通断电FE04", "01 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1A")
    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 00 01 00 02 00 01 01 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")
    engine.send_did("WRITE", "22V通断电FE04", "00 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1A")
    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")

    # 通道3
    engine.send_did("WRITE", "22V通断电FE04", "01 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1A")
    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 00 01 00 02 00 01 00 03 00 01 01 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")
    engine.send_did("WRITE", "22V通断电FE04", "00 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1A")

    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")

    # 通道4
    engine.send_did("WRITE", "22V通断电FE04", "01 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1A")
    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 01 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")
    engine.send_did("WRITE", "22V通断电FE04", "00 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1A")
    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")

    # 通道5
    engine.send_did("WRITE", "22V通断电FE04", "01 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1A")
    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 01 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")
    engine.send_did("WRITE", "22V通断电FE04", "00 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1A")

    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")

    # 通道6
    engine.send_did("WRITE", "22V通断电FE04", "01 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1A")
    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 01 07 00 01 00 08 00 01 00 09 00 01 00")
    engine.send_did("WRITE", "22V通断电FE04", "00 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1A")

    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")

    # 通道7
    engine.send_did("WRITE", "22V通断电FE04", "01 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1A")
    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 01 08 00 01 00 09 00 01 00")
    engine.send_did("WRITE", "22V通断电FE04", "00 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1A")

    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")

    # 通道8
    engine.send_did("WRITE", "22V通断电FE04", "01 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1A")
    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 01 09 00 01 00")
    engine.send_did("WRITE", "22V通断电FE04", "00 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1A")

    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")

    # 通道9
    engine.send_did("WRITE", "22V通断电FE04", "01 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1A")
    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 01")
    engine.send_did("WRITE", "22V通断电FE04", "00 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1A")

    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")

    # 使用FFA2数据标识读取，返回数据与D200相同；

    engine.send_FE02_did("WRITE", "IO配置D201", "01 00 02 00 03 00 04 00 05 00 06 00 07 00 08 00 09 00")
    engine.expect_FE02_did("WRITE", "IO配置D201", "01 00 02 00 03 00 04 00 05 00 06 00 07 00 08 00 09 00")
    # 通道1
    engine.send_did("WRITE", "22V通断电FE04", "01 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1A")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 00 01 01 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")
    engine.send_did("WRITE", "22V通断电FE04", "00 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1A")

    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")

    # 通道2
    engine.send_did("WRITE", "22V通断电FE04", "01 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1A")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 00 01 00 02 00 01 01 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")
    engine.send_did("WRITE", "22V通断电FE04", "00 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1A")

    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")

    # 通道3
    engine.send_did("WRITE", "22V通断电FE04", "01 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1A")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 00 01 00 02 00 01 00 03 00 01 01 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")
    engine.send_did("WRITE", "22V通断电FE04", "00 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1A")

    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")

    # 通道4
    engine.send_did("WRITE", "22V通断电FE04", "01 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1A")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 01 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")
    engine.send_did("WRITE", "22V通断电FE04", "00 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1A")

    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")

    # 通道5
    engine.send_did("WRITE", "22V通断电FE04", "01 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1A")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 01 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")
    engine.send_did("WRITE", "22V通断电FE04", "00 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1A")

    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")

    # 通道6
    engine.send_did("WRITE", "22V通断电FE04", "01 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1A")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 01 07 00 01 00 08 00 01 00 09 00 01 00")
    engine.send_did("WRITE", "22V通断电FE04", "00 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1A")

    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")

    # 通道7
    engine.send_did("WRITE", "22V通断电FE04", "01 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1A")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 01 08 00 01 00 09 00 01 00")
    engine.send_did("WRITE", "22V通断电FE04", "00 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1A")

    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")

    # 通道8
    engine.send_did("WRITE", "22V通断电FE04", "01 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1A")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 01 09 00 01 00")
    engine.send_did("WRITE", "22V通断电FE04", "00 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1A")

    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")

    # 通道9
    engine.send_did("WRITE", "22V通断电FE04", "01 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1A")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 01")
    engine.send_did("WRITE", "22V通断电FE04", "00 1A")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1A")

    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")

    # 数字输入模式不配置数据设置，用D200写数据返回错误，FFA2不支持写操作，也回复错误；
    engine.send_FE02_did("WRITE", "读IO点位数据FFA2",
                         "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")
    engine.expect_FE02_did("WRITE", "IO操作D200", "03 00")
    engine.send_FE02_did("WRITE", "读IO点位数据FFA2",
                         "01 00 01 00 02 00 01 00 03 00 01 00 04 00 01 00 05 00 01 00 06 00 01 00 07 00 01 00 08 00 01 00 09 00 01 00")
    engine.expect_FE02_did("WRITE", "读IO点位数据FFA2", "03 00")


def test_无源电子开关输出模式测试():
    """
     13_无源电子开关输出模式测试D201
     设备的所有通道均支持设置为数字输出模式：0x01-0x03，电磁继电器-0x01、磁保持继电器（正向闭合）-0x02、磁保持继电器（反向闭合）- 0x03。
     数字输出模式下支持数据的设置和读取；数据内容0x01表示继电器闭合，0x00表示继电器断开，0xFF表示无效状态（模式切换为数字输出时默认为此状态）。
    """

    # 通道模式变更，且变化为数字输出模式时，设备默认当前输出为0xFF即无效状态
    engine.send_FE02_did("WRITE", "IO配置D201", "02 20")
    engine.expect_FE02_did("WRITE", "IO配置D201", "02 20")
    engine.send_FE02_did("READ", "IO配置D201", "02")
    engine.expect_FE02_did("READ", "IO配置D201", "02 01")
    engine.send_FE02_did("WRITE", "IO配置D201", "02 01")
    engine.expect_FE02_did("WRITE", "IO配置D201", "02 01")
    engine.send_FE02_did("READ", "IO配置D201", "02")
    engine.expect_FE02_did("READ", "IO配置D201", "02 01")
    engine.send_FE02_did("READ", "IO操作D200", "02")
    engine.expect_FE02_did("READ", "IO操作D200", "02 01 01 00")

    # 只有在进行输出控制后，读取状态为闭合、断开状态；
    engine.send_FE02_did("WRITE", "IO配置D201", "02 01")
    engine.expect_FE02_did("WRITE", "IO配置D201", "02 01")
    engine.send_FE02_did("WRITE", "IO操作D200", "02 01 01 01")
    engine.expect_FE02_did("WRITE", "IO操作D200", "02 01 01 01")
    engine.send_FE02_did("READ", "IO操作D200", "02")
    engine.expect_FE02_did("READ", "IO操作D200", "02 01 01 01")

    engine.send_FE02_did("WRITE", "IO操作D200", "02 01 01 00")
    engine.expect_FE02_did("WRITE", "IO操作D200", "02 01 01 00")
    engine.send_FE02_did("READ", "IO操作D200", "02")
    engine.expect_FE02_did("READ", "IO操作D200", "02 01 01 00")

    # 若发送配置通道模式控制，但未改变模式类型，设备认为无变化，状态仍为原状态
    engine.send_FE02_did("WRITE", "IO操作D200", "02 01 01 01")
    engine.expect_FE02_did("WRITE", "IO操作D200", "02 01 01 01")
    engine.send_FE02_did("READ", "IO操作D200", "02")
    engine.expect_FE02_did("READ", "IO操作D200", "02 01 01 01")
    engine.send_FE02_did("READ", "IO配置D201", "02")
    engine.expect_FE02_did("READ", "IO配置D201", "02 01")
    engine.send_FE02_did("WRITE", "IO配置D201", "02 01")
    engine.expect_FE02_did("WRITE", "IO配置D201", "02 01")
    engine.send_FE02_did("READ", "IO操作D200", "02")
    engine.expect_FE02_did("READ", "IO操作D200", "02 01 01 01")

    # 7.5.1.无源电子开关输出
    #设置所有通道均为电磁继电器模式；
    engine.send_FE02_did("WRITE", "IO配置D201", "01 01 02 01 03 01 04 01 05 01 06 01 07 01 08 01 09 01")
    engine.expect_FE02_did("WRITE", "IO配置D201", "01 01 02 01 03 01 04 01 05 01 06 01 07 01 08 01 09 01")
    engine.send_FE02_did("READ", "IO配置D201", "00")
    engine.expect_FE02_did("READ", "IO配置D201", "01 01 02 01 03 01 04 01 05 01 06 01 07 01 08 01 09 01")

    # 断电后重新读取模式；
    engine.send_did("WRITE", "22V通断电FE04", "00 20")
    engine.expect_did("WRITE", "22V通断电FE04", "00 20")
    engine.wait(5, allowed_message=True)
    engine.send_did("WRITE", "22V通断电FE04", "01 20")
    engine.expect_did("WRITE", "22V通断电FE04", "01 20")
    engine.wait(5, allowed_message=True)
    # engine.send_FE02_did("WRITE", "IO配置D201", "01 01 02 01 03 01 04 01 05 01 06 01 07 01 08 01 09 01")
    # engine.expect_FE02_did("WRITE", "IO配置D201", "01 01 02 01 03 01 04 01 05 01 06 01 07 01 08 01 09 01")
    engine.send_FE02_did("READ", "IO配置D201", "00")
    engine.expect_FE02_did("READ", "IO配置D201", "01 01 02 01 03 01 04 01 05 01 06 01 07 01 08 01 09 01")

    # 模式变化后，读取设备数据，变化后为无效状态0x00；
    engine.send_FE02_did("WRITE", "IO配置D201", "01 20 02 20 03 20 04 20 05 20 06 20 07 20 08 20 09 20")
    engine.expect_FE02_did("WRITE", "IO配置D201", "01 20 02 20 03 20 04 20 05 20 06 20 07 20 08 20 09 20")
    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 20 02 00 00 00 00 02 20 02 00 00 00 00 03 20 02 00 00 00 00 04 20 02 00 00 00 00 05 20 02 00 00 00 00 06 20 02 00 00 00 00 07 20 02 00 00 00 00 08 20 02 00 00 00 00 09 20 02 00 00 00 00")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 20 02 00 00 00 00 02 20 02 00 00 00 00 03 20 02 00 00 00 00 04 20 02 00 00 00 00 05 20 02 00 00 00 00 06 20 02 00 00 00 00 07 20 02 00 00 00 00 08 20 02 00 00 00 00 09 20 02 00 00 00 00")

    # 设置通道数据使继电器闭合，并读取继电器状态；
    engine.send_FE02_did("WRITE", "IO操作D200",
                         "01 01 01 01 02 01 01 01 03 01 01 01 04 01 01 01 05 01 01 01 06 01 01 01 07 01 01 01 08 01 01 01 09 01 01 01")
    engine.expect_FE02_did("WRITE", "IO操作D200",
                           "01 01 01 01 02 01 01 01 03 01 01 01 04 01 01 01 05 01 01 01 06 01 01 01 07 01 01 01 08 01 01 01 09 01 01 01")

    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 01 01 01 02 01 01 01 03 01 01 01 04 01 01 01 05 01 01 01 06 01 01 01 07 01 01 01 08 01 01 01 09 01 01 01")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 01 01 01 02 01 01 01 03 01 01 01 04 01 01 01 05 01 01 01 06 01 01 01 07 01 01 01 08 01 01 01 09 01 01 01")

    # 设置通道数据使继电器断开，并读取继电器状态；
    engine.send_FE02_did("WRITE", "读IO点位数据FFA2",
                         "01 01 01 00 02 01 01 00 03 01 01 00 04 01 01 00 05 01 01 00 06 01 01 00 07 01 01 00 08 01 01 00 09 01 01 00")
    engine.expect_FE02_did("WRITE", "读IO点位数据FFA2", "04 00")
    engine.send_FE02_did("WRITE", "IO操作D200",
                         "01 01 01 00 02 01 01 00 03 01 01 00 04 01 01 00 05 01 01 00 06 01 01 00 07 01 01 00 08 01 01 00 09 01 01 00")
    engine.expect_FE02_did("WRITE", "IO操作D200",
                           "01 01 01 00 02 01 01 00 03 01 01 00 04 01 01 00 05 01 01 00 06 01 01 00 07 01 01 00 08 01 01 00 09 01 01 00")

    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 01 01 00 02 01 01 00 03 01 01 00 04 01 01 00 05 01 01 00 06 01 01 00 07 01 01 00 08 01 01 00 09 01 01 00")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 01 01 00 02 01 01 00 03 01 01 00 04 01 01 00 05 01 01 00 06 01 01 00 07 01 01 00 08 01 01 00 09 01 01 00")



    # 7.5.2.无源电子开关输出（正向导通、负向关断）

    # 设置所有通道均为磁保持继电器（正向闭合）模式；
    engine.send_FE02_did("WRITE", "IO配置D201", "01 02 02 02 03 02 04 02 05 02 06 02 07 02 08 02 09 02")
    engine.expect_FE02_did("WRITE", "IO配置D201", "01 02 02 02 03 02 04 02 05 02 06 02 07 02 08 02 09 02")
    engine.send_FE02_did("READ", "IO配置D201", "00")
    engine.expect_FE02_did("READ", "IO配置D201", "01 02 02 02 03 02 04 02 05 02 06 02 07 02 08 02 09 02")

    # 断电后重新读取模式；
    engine.send_did("WRITE", "22V通断电FE04", "00 20")
    engine.expect_did("WRITE", "22V通断电FE04", "00 20")
    engine.wait(5, allowed_message=True)
    engine.send_did("WRITE", "22V通断电FE04", "01 20")
    engine.expect_did("WRITE", "22V通断电FE04", "01 20")
    engine.wait(5, allowed_message=True)
    engine.send_FE02_did("READ", "IO配置D201", "00")
    engine.expect_FE02_did("READ", "IO配置D201", "01 02 02 02 03 02 04 02 05 02 06 02 07 02 08 02 09 02")

    # 模式变化后，读取设备数据，变化后为无效状态0x00
    engine.send_FE02_did("WRITE", "IO配置D201", "01 01 02 01 03 01 04 01 05 01 06 01 07 01 08 01 09 01")
    engine.expect_FE02_did("WRITE", "IO配置D201", "01 01 02 01 03 01 04 01 05 01 06 01 07 01 08 01 09 01")
    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 01 01 00 02 01 01 00 03 01 01 00 04 01 01 00 05 01 01 00 06 01 01 00 07 01 01 00 08 01 01 00 09 01 01 00")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 01 01 00 02 01 01 00 03 01 01 00 04 01 01 00 05 01 01 00 06 01 01 00 07 01 01 00 08 01 01 00 09 01 01 00")

    # 设置通道数据使继电器闭合，并读取继电器状态；
    engine.send_FE02_did("WRITE", "IO操作D200",
                         "01 02 01 01 02 02 01 01 03 02 01 01 04 02 01 01 05 02 01 01 06 02 01 01 07 02 01 01 08 02 01 01 09 02 01 01")
    engine.expect_FE02_did("WRITE", "IO操作D200",
                           "01 02 01 01 02 02 01 01 03 02 01 01 04 02 01 01 05 02 01 01 06 02 01 01 07 02 01 01 08 02 01 01 09 02 01 01")

    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 02 01 01 02 02 01 01 03 02 01 01 04 02 01 01 05 02 01 01 06 02 01 01 07 02 01 01 08 02 01 01 09 02 01 01")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 02 01 01 02 02 01 01 03 02 01 01 04 02 01 01 05 02 01 01 06 02 01 01 07 02 01 01 08 02 01 01 09 02 01 01")

    # 设置通道数据使继电器断开，并读取继电器状态；
    engine.send_FE02_did("WRITE", "IO操作D200",
                         "01 02 01 00 02 02 02 00 03 02 01 00 04 02 01 00 05 02 01 00 06 02 01 00 07 02 01 00 08 02 01 00 09 02 01 00")
    engine.expect_FE02_did("WRITE", "IO操作D200",
                           "01 02 01 00 02 02 02 00 03 02 01 00 04 02 01 00 05 02 01 00 06 02 01 00 07 02 01 00 08 02 01 00 09 02 01 00")
    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 02 01 00 02 02 02 00 03 02 01 00 04 02 01 00 05 02 01 00 06 02 01 00 07 02 01 00 08 02 01 00 09 02 01 00")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 02 01 00 02 02 02 00 03 02 01 00 04 02 01 00 05 02 01 00 06 02 01 00 07 02 01 00 08 02 01 00 09 02 01 00")

    # 7.5.3.无源电子开关输出（负向导通、正向关断）

    # 设置所有通道均为磁保持继电器（反向闭合）模式；
    engine.send_FE02_did("WRITE", "IO配置D201", "01 03 02 03 03 03 04 03 05 03 06 03 07 03 08 03 09 03")
    engine.expect_FE02_did("WRITE", "IO配置D201", "01 03 02 03 03 03 04 03 05 03 06 03 07 03 08 03 09 03")
    engine.send_FE02_did("READ", "IO配置D201", "00")
    engine.expect_FE02_did("READ", "IO配置D201", "01 03 02 03 03 03 04 03 05 03 06 03 07 03 08 03 09 03")

    # 断电后重新读取模式；
    engine.send_did("WRITE", "22V通断电FE04", "00 20")
    engine.expect_did("WRITE", "22V通断电FE04", "00 20")
    engine.wait(20, allowed_message=True)
    engine.send_did("WRITE", "22V通断电FE04", "01 20")
    engine.expect_did("WRITE", "22V通断电FE04", "01 20")
    engine.wait(5, allowed_message=True)
    engine.send_FE02_did("READ", "IO配置D201", "00")
    engine.expect_FE02_did("READ", "IO配置D201", "01 03 02 03 03 03 04 03 05 03 06 03 07 03 08 03 09 03")

    # 模式变化后，读取设备数据，变化后为无效状态0x00；
    engine.send_FE02_did("WRITE", "IO配置D201", "01 01 02 01 03 01 04 01 05 01 06 01 07 01 08 01 09 01")
    engine.expect_FE02_did("WRITE", "IO配置D201", "01 01 02 01 03 01 04 01 05 01 06 01 07 01 08 01 09 01")
    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 01 01 00 02 01 01 00 03 01 01 00 04 01 01 00 05 01 01 00 06 01 01 00 07 01 01 00 08 01 01 00 09 01 01 00")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 01 01 00 02 01 01 00 03 01 01 00 04 01 01 00 05 01 01 00 06 01 01 00 07 01 01 00 08 01 01 00 09 01 01 00")

    # 设置通道数据使继电器闭合，并读取继电器状态；
    engine.send_FE02_did("WRITE", "IO操作D200",
                         "01 03 01 01 02 03 01 01 03 03 01 01 04 03 01 01 05 03 01 01 06 03 01 01 07 03 01 01 08 03 01 01 09 03 01 01")
    engine.expect_FE02_did("WRITE", "IO操作D200",
                           "01 03 01 01 02 03 01 01 03 03 01 01 04 03 01 01 05 03 01 01 06 03 01 01 07 03 01 01 08 03 01 01 09 03 01 01")

    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 03 01 01 02 03 01 01 03 03 01 01 04 03 01 01 05 03 01 01 06 03 01 01 07 03 01 01 08 03 01 01 09 03 01 01")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 03 01 01 02 03 01 01 03 03 01 01 04 03 01 01 05 03 01 01 06 03 01 01 07 03 01 01 08 03 01 01 09 03 01 01")

    # 设置通道数据使继电器断开，并读取继电器状态；
    engine.send_FE02_did("WRITE", "IO操作D200",
                         "01 03 01 00 02 03 02 00 03 03 01 00 04 03 01 00 05 03 01 00 06 03 01 00 07 03 01 00 08 03 01 00 09 03 01 00")
    engine.expect_FE02_did("WRITE", "IO操作D200",
                           "01 03 01 00 02 03 02 00 03 03 01 00 04 03 01 00 05 03 01 00 06 03 01 00 07 03 01 00 08 03 01 00 09 03 01 00")
    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 03 01 00 02 03 02 00 03 03 01 00 04 03 01 00 05 03 01 00 06 03 01 00 07 03 01 00 08 03 01 00 09 03 01 00")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 03 01 00 02 03 02 00 03 03 01 00 04 03 01 00 05 03 01 00 06 03 01 00 07 03 01 00 08 03 01 00 09 03 01 00")


def test_模拟输入模式测试():
    """
     13_模拟输入模式测试D201
     设备的所有通道均支持设置为模拟输入模式，设备支持的模拟输入类型有：
     1.NTC10K-B3435									0x20
     2.NTC10K-B3950									0x21
     3.PT1000									    0x22
     4.NI1000									    0x23
     5.NTC20K-B3950									0x24
     6.NTC100K-B3950								0x25
     7.0-10V输出									    0xC0
     8.4-20mA输出									0xE0
    """

    # 7.6.1.0-10V输入
    # 设置所有通道均为0-10V输入模式；
    engine.send_FE02_did("WRITE", "IO配置D201", "01 40 02 40 03 40 04 40 05 40 06 40 07 40 08 40 09 40")
    engine.expect_FE02_did("WRITE", "IO配置D201", "01 40 02 40 03 40 04 40 05 40 06 40 07 40 08 40 09 40")
    engine.send_FE02_did("READ", "IO配置D201", "00")
    engine.expect_FE02_did("READ", "IO配置D201", "01 40 02 40 03 40 04 40 05 40 06 40 07 40 08 40 09 40")

    # 断电后重新读取模式；
    engine.send_did("WRITE", "22V通断电FE04", "00 20")
    engine.expect_did("WRITE", "22V通断电FE04", "00 20")
    engine.wait(20, allowed_message=True)
    engine.send_did("WRITE", "22V通断电FE04", "01 20")
    engine.expect_did("WRITE", "22V通断电FE04", "01 20")
    engine.wait(5, allowed_message=True)
    engine.send_FE02_did("READ", "IO配置D201", "00")
    engine.expect_FE02_did("READ", "IO配置D201", "01 40 02 40 03 40 04 40 05 40 06 40 07 40 08 40 09 40")

    # 各通道均未接入电压，读取数据全为十几mV；
    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 40 02 ** ** 00 00 02 40 02 ** ** 00 00 03 40 02 ** ** 00 00 04 40 02 ** ** 00 00 05 40 02 ** ** 00 00 06 40 02 ** ** 00 00 07 40 02 ** ** 00 00 08 40 02 ** ** 00 00 09 40 02 ** ** 00 00")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 40 02 ** ** ** 00 00 02 40 02 ** ** ** 00 00 03 40 02 ** ** ** 00 00 04 40 02 ** ** ** 00 00 05 40 02 ** ** ** 00 00 06 40 02 ** ** ** 00 00 07 40 02 ** ** ** 00 00 08 40 02 ** ** ** 00 00 09 40 02 ** ** ** 00 00")


    # engine.send_did("WRITE", "22V通断电FE04", "01 09")
    # engine.expect_did("WRITE", "22V通断电FE04", "01 09")

    #将通道1、2、3分别接入1V测试;(误差未写)
    engine.send_did("WRITE", "22V通断电FE04", "01 1E")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1E")
    engine.send_did("WRITE", "工装软件版本FE05", "01 01")
    engine.expect_did("WRITE", "工装软件版本FE05", "01 01")

    engine.send_FE02_did("READ", "IO操作D200", "01 02 03")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 40 02 ** ** 10 00 02 40 02 ** ** 10 00 03 40 02 ** ** 10 00")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "01 02 03")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 40 02 ** ** ** 10 00 02 40 02 ** ** ** 10 00 03 40 02 ** ** ** 10 00")
    engine.send_did("WRITE", "22V通断电FE04", "00 1E")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1E")



    #将通道4、5、6分别接入5V测试；(误差未写)
    engine.send_did("WRITE", "22V通断电FE04", "01 1E")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1E")
    engine.send_did("WRITE", "工装软件版本FE05", "01 02")
    engine.expect_did("WRITE", "工装软件版本FE05", "01 02")

    engine.send_FE02_did("READ", "IO操作D200", "04 05 06")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 40 02 ** ** 10 00 02 40 02 ** ** 10 00 03 40 02 ** ** 10 00")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "04 05 06")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 40 02 ** ** ** 10 00 02 40 02 ** ** ** 10 00 03 40 02 ** ** ** 10 00")
    engine.send_did("WRITE", "22V通断电FE04", "00 1E")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1E")

    # 将通道4、5、6分别接入10V测试；(误差未写)
    engine.send_did("WRITE", "22V通断电FE04", "01 1E")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1E")
    engine.send_did("WRITE", "工装软件版本FE05", "01 03")
    engine.expect_did("WRITE", "工装软件版本FE05", "01 03")

    engine.send_FE02_did("READ", "IO操作D200", "07 08 09")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 40 02 ** ** 10 00 02 40 02 ** ** 10 00 03 40 02 ** ** 10 00")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "07 08 09")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 40 02 ** ** ** 10 00 02 40 02 ** ** ** 10 00 03 40 02 ** ** ** 10 00")
    engine.send_did("WRITE", "22V通断电FE04", "00 1E")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1E")


    #对于超范围数据设备回复全FF表示数据越限，为保证越限冗余，当设备检测电压输入超过11V则认为越限；(问问李鹏)
    engine.send_FE02_did("READ", "IO操作D200", "07 08 09")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 40 02 FF FF FF FF 02 40 02 FF FF FF FF 03 40 02 FF FF FF FF")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "07 08 09")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 40 02 FF FF FF FF FF 02 40 02 FF FF FF FF FF 03 40 02 FF FF FF FF FF")

    # 7.6.2.4-20mA输入
    # 7.6.2.4-20mA输入；
    engine.send_FE02_did("WRITE", "IO配置D201", "01 60 02 60 03 60 04 60 05 60 06 60 07 60 08 60 09 60")
    engine.expect_FE02_did("WRITE", "IO配置D201", "01 60 02 60 03 60 04 60 05 60 06 60 07 60 08 60 09 60")
    engine.send_FE02_did("READ", "IO配置D201", "00")
    engine.expect_FE02_did("READ", "IO配置D201", "01 60 02 60 03 60 04 60 05 60 06 60 07 60 08 60 09 60")

    # 断电后重新读取模式；
    engine.send_did("WRITE", "22V通断电FE04", "00 20")
    engine.expect_did("WRITE", "22V通断电FE04", "00 20")
    engine.wait(20, allowed_message=True)
    engine.send_did("WRITE", "22V通断电FE04", "01 20")
    engine.expect_did("WRITE", "22V通断电FE04", "01 20")
    engine.wait(5, allowed_message=True)
    engine.send_FE02_did("READ", "IO配置D201", "00")
    engine.expect_FE02_did("READ", "IO配置D201", "01 60 02 60 03 60 04 60 05 60 06 60 07 60 08 60 09 60")

    # 各通道均未接入电流，读取数据全为0；
    engine.send_FE02_did("READ", "IO操作D200", "00")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 60 02 00 00 00 00 02 60 02 00 00 00 00 03 60 02 00 00 00 00 04 60 02 00 00 00 00 05 60 02 00 00 00 00 06 60 02 00 00 00 00 07 60 02 00 00 00 00 08 60 02 00 00 00 00 09 60 02 00 00 00 00")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "00")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 60 02 01 00 00 00 00 02 60 02 01 00 00 00 00 03 60 02 01 00 00 00 00 04 60 02 01 00 00 00 00 05 60 02 01 00 00 00 00 06 60 02 01 00 00 00 00 07 60 02 01 00 00 00 00 08 60 02 01 00 00 00 00 09 60 02 01 00 00 00 00")



    # 将通道1、2、3分别接入2mA测试；(误差未写)(未写)
    engine.send_did("WRITE", "22V通断电FE04", "01 1F")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1F")
    engine.send_did("WRITE", "工装软件版本FE05", "02 01")
    engine.expect_did("WRITE", "工装软件版本FE05", "02 01")

    engine.send_FE02_did("READ", "IO操作D200", "01 02 03")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 40 02 ** ** 10 00 02 40 02 ** ** 10 00 03 40 02 ** ** 10 00")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "01 02 03")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 40 02 ** ** ** 10 00 02 40 02 ** ** ** 10 00 03 40 02 ** ** ** 10 00")
    engine.send_did("WRITE", "22V通断电FE04", "00 1E")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1E")

    # 将通道4、5、6分别接入5V测试；(误差未写)
    engine.send_did("WRITE", "22V通断电FE04", "01 1E")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1E")
    engine.send_did("WRITE", "工装软件版本FE05", "01 02")
    engine.expect_did("WRITE", "工装软件版本FE05", "01 02")
    engine.send_FE02_did("WRITE", "IO配置D201", "04 40 05 40 06 40")
    engine.expect_FE02_did("WRITE", "IO配置D201", "04 40 05 40 06 40")

    engine.send_FE02_did("READ", "IO操作D200", "04 05 06")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 40 02 ** ** 10 00 02 40 02 ** ** 10 00 03 40 02 ** ** 10 00")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "04 05 06")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 40 02 ** ** ** 10 00 02 40 02 ** ** ** 10 00 03 40 02 ** ** ** 10 00")
    engine.send_did("WRITE", "22V通断电FE04", "00 1E")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1E")

    # 将通道4、5、6分别接入10V测试；(误差未写)
    engine.send_did("WRITE", "22V通断电FE04", "01 1E")
    engine.expect_did("WRITE", "22V通断电FE04", "01 1E")
    engine.send_did("WRITE", "工装软件版本FE05", "01 03")
    engine.expect_did("WRITE", "工装软件版本FE05", "01 03")
    engine.send_FE02_did("WRITE", "IO配置D201", "07 40 08 40 09 40")
    engine.expect_FE02_did("WRITE", "IO配置D201", "07 40 08 40 09 40")

    engine.send_FE02_did("READ", "IO操作D200", "07 08 09")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 40 02 ** ** 10 00 02 40 02 ** ** 10 00 03 40 02 ** ** 10 00")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "07 08 09")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 40 02 ** ** ** 10 00 02 40 02 ** ** ** 10 00 03 40 02 ** ** ** 10 00")
    engine.send_did("WRITE", "22V通断电FE04", "00 1E")
    engine.expect_did("WRITE", "22V通断电FE04", "00 1E")

    # 对于超范围数据设备回复全FF表示数据越限，为保证越限冗余，当设备检测电压输入超过11V则认为越限；(问问李鹏)
    engine.send_FE02_did("READ", "IO操作D200", "07 08 09")
    engine.expect_FE02_did("READ", "IO操作D200",
                           "01 40 02 FF FF FF FF 02 40 02 FF FF FF FF 03 40 02 FF FF FF FF")
    engine.send_FE02_did("READ", "读IO点位数据FFA2", "07 08 09")
    engine.expect_FE02_did("READ", "读IO点位数据FFA2",
                           "01 40 02 FF FF FF FF FF 02 40 02 FF FF FF FF FF 03 40 02 FF FF FF FF FF")
