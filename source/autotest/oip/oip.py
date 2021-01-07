#encoding:utf-8
import engine

# 配置测试基本参数
config = dict()
config["测试程序名称"] = r"ESSN-OIP-A(v1.1)-20200901"
config["串口"] = "COM14"
config["波特率"] = "9600"
config["校验位"] = 'None'
config["抄控器默认源地址"] = 1
config["测试设备地址"] = 464148
config["设备PWD000A"] = 55013
config["panid"] = 22


# 定义测试设备的基本信息
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
# 定义前置通断电工装AID和PWD
config["前置通断电工装AID"] = 778856
config["前置通断电工装PWD"] = 39751
engine.config(config)

if __name__ == "__main__":
    import os
    engine.set_output_dir(os.path.dirname(__file__))
    engine.run_all_tests(gui=True)