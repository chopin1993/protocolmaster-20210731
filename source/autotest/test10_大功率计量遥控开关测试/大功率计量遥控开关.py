# encoding:utf-8
# 导入测试引擎
import engine

# 配置测试报告基本信息
config = dict()
config["测试程序名称"] = r"大功率计量遥控开关ESEM-1S63A-K-D35测试报告"
# 定义抄控器的基本信息
config["串口"] = "COM19"
config["波特率"] = "115200"     # 当前测试上位机，只支持9600bps和115200bps
config["校验位"] = 'None'
config["抄控器默认源地址"] = 91
config["panid"] = 0  # 平板网关展架：14168；平板网关MAX：11176；三相智能网关展架：9113
# 定义测试设备的基本信息
config["测试设备地址"] = 594013
config["设备PWD000A"] = 37904
config["设备类型0001"] = "FF FF 1D 00 00 00 01 00"
config["应用层通讯协议及版本0002"] = "EASTSOFT(v1.0)"
config["设备描述信息设备制造商0003"] = r"ESEM-1S63A-K-D35(v1.2)-20210602"
config["DKEY0005"] = "0000FE05"
config["SN0007"] = "31 74 10 20 00 62 12 21 99 00 00 01"
# 定义测试设备所用的1663载波模块的基本信息
config["载波版本号0004"] = "SSC1663-ADPT-V30A014"
config["适配层物料编码0602"] = "83676800004"
config["适配层版本号0606"] = "ESMD-AD63(v2.2)-20170826"
config["网络层物料编码0609"] = "83676800003"
config["网络层版本号060A"] = "SSC1663-PLC(v1.0)-20171011"
# 定义测试设备所用的1667载波模块的基本信息
# config["载波版本号0004"] = "SSC1667-ADPT-V30B011"
# config["适配层物料编码0602"] = "83676800205"
# config["适配层版本号0606"] = "ESMD-AD6768(v1.2)-20200701"
# config["网络层物料编码0609"] = "83676800202"
# config["网络层版本号060A"] = "SSC1667-PLC(v5.0)-20190907"
# 定义被测设备上电后初始化时间
config["被测设备上电后初始化时间"] = 15
# 定义被测设备类型默认为继电器版硬件
config["被测设备硬件版本"] = "63A版本"    # 32A版本

config["应用程序上一版发布版本"] = r"ESEM-1S63A-K-D35(v1.1)-20180412"  # 如果此处为空字符串时，表示不支持兼容性升级或手动测试。
config["应用程序同版本号测试版本"] = r"ESTK-03(v2.0)-20210520"
# 根据被测设备不同的载波版本，分别设置1663和1667参数
config["载波适配层上一版本"] = "ESMD-AD63(v2.1)-20170210"
config["载波网络层上一版本"] = "SSC1663-PLC(v1.0)-20170510"
# config["载波适配层上一版本"] = "ESMD-AD6768(v1.1)-20180706"
# config["载波网络层上一版本"] = "SSC1667-PLC(v5.0)-20180706"
config["升级后等待重启时间"] = 15  # 默认30s，可根据具体设备升级后重启时间为例修改

# 增加测试循环次数
config["test_loop_times"] = 1

engine.config(config)

if __name__ == "__main__":
    import os

    # 设置测试文档的输出目录，默认输出到 开关控制模块 文件夹下
    engine.set_output_dir(os.path.dirname(__file__))
    engine.run_all_tests(gui=True)
