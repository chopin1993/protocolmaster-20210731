from enum import Enum

class TstEnum(Enum):
    ENUM1 = 1
    ENUM2 = 2
    ENUM3 = 3
    
def testEnum():
    # ����ö�ٳ�Ա
    print("all members")
    for e in TstEnum:
        print(e)
    # ͨ��ֵ��ȡö�ٳ�Ա
    data = TstEnum(value=1)
    print(data,data.name, data.value)

    # ͨ�����ƻ�ȡö�ٳ�Ա
    data2 = TstEnum["ENUM2"]
    print(data2,data2.name,data2.value)
