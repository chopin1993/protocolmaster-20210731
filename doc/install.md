**安装指南： **

# 开发环境搭建指南
1. 安装python3.7版本
2. 安装pyqt5，版本固定为5.13.0，高版本在windows有不兼容bugs.
3. 安装pyqt-sip 
4. 安装pyqt5-tools，本将qtdesigner和uci配置为pycharm集成开发工具。


# 安装指南


# 环境导出和使用指南
```shell
#D:\python3.7\Scripts\pip.exe freeze > requirement.txt
pip freeze > requirements.txt
pip install -r requirements.txt
```

# 常见问题
serailExcepiton
需要将serial和pyserial卸载，然后重新安装pyserial
```shell script
pip uninstall  serial 
pip uninstall pyserial 
pip install serial 
```