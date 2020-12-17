# encoding = "UTF-8"
"""
1、AID转16进制，并且小端倒置
2、匹配函数
3、输出结果
"""


def get_os():
    """
    获取当前目录内的文件名列表，然后输出监控器搜索的文件名称
    """
    import os
    file_list = os.listdir()
    for i in file_list:
        if "ROUTEREXPORT" in i:
            path = i
            break
    return path


def aid_to_hex():
    """
    将文本内的AID，转换为16进制小端显示
    """
    fo = open(r"device_aid.txt", 'r')
    devices_list = list()
    for line in fo.readlines():  # 依次读取每行
        line = line.strip()  # 去掉每行头尾空白
        if line != "":
            line = hex(int(line)).upper()
            line = line.lstrip('0X').zfill(8)
            line = line[6:8] + line[4:6] + line[2:4] + line[0:2]
            devices_list.append(line)
    fo.close()
    return devices_list


def hex_to_aid(aid_hex):
    """
    将文本内的16进制小端显示,转换为AID
    """
    aid_hex = aid_hex[6:8] + aid_hex[4:6] + aid_hex[2:4] + aid_hex[0:2]
    aid = int(aid_hex, 16)
    aid = str(aid)
    return aid


def match_mac(aid):
    """
    在监控器搜索MAC地址的列表中，查询当期的aid匹配的mac，并输出
    :param aid:输入aid信息
    """
    path = get_os()
    fo = open(path, 'r')
    mac = "No_match".rjust(12)
    for line in fo.readlines():  # 依次读取每行
        # line = line.strip()  # 去掉每行头尾空白
        line.strip()  # 去掉每行头尾空白
        if line == "":  # 去掉空字符串
            continue
        if aid in line:
            line = line.split()
            mac = line[3]
            break
    fo.close()
    return mac


if __name__ == "__main__":

    result_file = open(r'./匹配结果.txt', 'w+',encoding="UTF-8")
    device_list = aid_to_hex()
    if len(device_list) == 0:
        result_file.write("未发现有效的AID")
    else:
        for i in device_list:
            result_file.write(match_mac(i) + "    0000    " + hex_to_aid(i) + "\n")
    result_file.close()
