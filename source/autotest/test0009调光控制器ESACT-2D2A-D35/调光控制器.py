# encoding:utf-8
# 导入测试引擎
import engine

# 配置测试报告基本信息
config = dict()
config["测试程序名称"] = r"test0009调光控制器ESACT-2D2A-D35.2)-20210315测试"
# 定义抄控器的基本信息
config["串口"] = "COM18"
config["波特率"] = "115200"  # 当前测试上位机，只支持9600bps和115200bps
config["校验位"] = 'None'
config["抄控器默认源地址"] = 11
config["panid"] = 9113  # 平板网关展架：14168；平板网关MAX：11176；三相智能网关展架：9113
# 定义测试设备的基本信息
config["测试设备地址"] = 49715
config["设备PWD000A"] = 2394
config["设备类型0001"] = "FF FF 14 00 00 00 02 00"
config["应用层通讯协议及版本0002"] = "EASTSOFT(v1.0)"
config["设备描述信息设备制造商0003"] = "ESACT-2D2A-D35(v1.1)-20191225"
config["DKEY0005"] = "00008ULX"
config["SN0007"] = "32 01 10 20 00 41 82 11 99 00 00 01"
# 定义测试设备所用的1663载波模块的基本信息
# config["载波版本号0004"] = "SSC1663-ADPT-V30A014"
# config["适配层物料编码0602"] = "83676800004"
# config["适配层版本号0606"] = "ESMD-AD63(v2.2)-20170826"
# config["网络层物料编码0609"] = "83676800003"
# config["网络层版本号060A"] = "SSC1663-PLC(v1.0)-20171011"
# 定义测试设备所用的1667载波模块的基本信息
config["载波版本号0004"] = "SSC1663-ADPT-V30A014"
config["适配层物料编码0602"] = "83676800004"
config["适配层版本号0606"] = "ESMD-AD6768(v1.2)-20200701"
config["网络层物料编码0609"] = "83676800205"
config["网络层版本号060A"] = "SSC1667-PLC(v5.0)-20190709"
# 定义被测设备上电后初始化时间
config["被测设备上电后初始化时间"] = 15.5
engine.config(config)

if __name__ == "__main__":
    import os

    # 设置测试文档的输出目录，默认输出到 开关控制模块 文件夹下
    engine.set_output_dir(os.path.dirname(__file__))
    engine.run_all_tests(gui=True)
