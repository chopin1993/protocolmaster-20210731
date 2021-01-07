import engine
from autotest.公共用例.public00init配置初始化 import *
from autotest.公共用例.public常用测试模块 import set_gw_info

def init_清空网关():
    "清空设备panid"
    set_gw_info(panid=0)


