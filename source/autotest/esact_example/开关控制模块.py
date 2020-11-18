#encoding:utf-8
# 导入测试引擎
import engine

#配置测试串口
config = dict()
config["测试程序名称"] = r"ESACT-1A(v1.4)-20171020"
config["串口"] = "COM9"
config["波特率"] = "9600"
config["校验位"] = 'None'
config["抄控器默认源地址"] = 1
config["测试设备地址"] = 76744
config["设备密码"] = 19443
config["panid"] = 0
engine.config(config)

if __name__ == "__main__":
    import os
    # 设置测试文档的输出目录，默认输出到 开关控制模块 文件夹下
    engine.set_output_dir(os.path.dirname(__file__))
    engine.run_all_tests(gui=True)