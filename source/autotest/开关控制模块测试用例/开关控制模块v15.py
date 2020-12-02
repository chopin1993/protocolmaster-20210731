# encoding:utf-8
# 导入测试引擎
import engine

# 配置测试报告基本信息
config = dict()
config["测试程序名称"] = r"ESACT-1A(v1.5)-20200805"
# 定义抄控器的基本信息
config["串口"] = "COM6"
config["波特率"] = "9600"
config["校验位"] = 'None'
config["抄控器默认源地址"] = 20
config["panid"] = 1000  # 平板网关展架：14168；平板网关MAX：11176；三相智能网关展架：9113
# 定义测试设备的基本信息
config["测试设备地址"] = 607359
config["设备PWD000A"] = 17795
config["设备类型0001"] = "FF FF 18 00 01 00 01 00"
config["应用层通讯协议及版本0002"] = "EASTSOFT(v1.0)"
config["设备描述信息设备制造商0003"] = "ESACT-1A(v1.5)-20200805"
config["DKEY0005"] = "00000ZXU"
config["SN0007"] = "31 71 10 10 00 51 65 01 01 00 01 48"
# 定义测试设备所用的载波模块的基本信息
config["载波版本号0004"] = "SSC1663-ADPT-V30A014"
config["适配层物料编码0602"] = "83676800004"
config["适配层版本号0606"] = "ESMD-AD63(v2.2)-20170826"
config["网络层物料编码0609"] = "83676800003"
config["网络层版本号060A"] = "SSC1663-PLC(v1.0)-20171011"
engine.config(config)

if __name__ == "__main__":
    import os

    # 设置测试文档的输出目录，默认输出到 开关控制模块 文件夹下
    engine.set_output_dir(os.path.dirname(__file__))
    engine.run_all_tests(gui=True)
