#encoding:utf-8
# 导入测试引擎
import engine

#配置测试串口
config = dict()
config["测试程序名称"] = "ESACT-1A(v1.5)-20200808"
config["串口"] = "COM14"
config["波特率"] = "9600"
config["校验位"] = 'None'
config["抄控器默认源地址"] = 20
config["测试设备地址"] = 413246
config["设备PWD000A"] = 11948
config["panid"] = 30
engine.config(config)

if __name__ == "__main__":
    import os
    # 设置测试文档的输出目录，默认输出到 开关控制模块 文件夹下
    engine.set_output_dir(os.path.dirname(__file__))
    engine.run_all_tests(gui=True)