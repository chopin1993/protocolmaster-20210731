#encoding:utf-8

from enum import Enum

class TstEnum(Enum):
    ENUM1 = 1
    ENUM2 = 2
    ENUM3 = 3
    
def testEnum():
    # 遍历枚举成员
    print("all members")
    for e in TstEnum:
        print(e)
    # 通过值获取枚举成员
    data = TstEnum(value=1)
    print(data, data.name, data._value)

    # 通过名称获取枚举成员
    data2 = TstEnum["ENUM2"]
    print(data2, data2.name, data2._value)

    try:
        TstEnum["ss"]
    except Exception as key:
        print("key error exception",str(key))

