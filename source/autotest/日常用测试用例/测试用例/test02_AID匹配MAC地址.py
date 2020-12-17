"""
1、AID转16进制，并且小端倒置
2、匹配函数
3、输出结果
"""
# from codecs import open


def match_mac(aid):
    path = r"C:/Users/SUN/Desktop/test/ROUTEREXPORT,  2020-12-16 14-14-35 - 副本.txt"
    fo = open(path, mode='r') #
    for line in fo.readlines():  # 依次读取每行
        line = line.strip()  # 去掉每行头尾空白
        if aid in line:
            line = line.split()
            mac = line[3]
            break
    fo.close()
    return mac


def aid_to_hex():
    path = r"C:/Users/SUN/Desktop/test/devices.txt"
    fo = open(path, mode='r')
    for line in fo.readlines():  # 依次读取每行
        line = line.strip()  # 去掉每行头尾空白
        line = hex(int(line)).upper()
        line = str(line).lstrip('0X').zfill(8)
        line = line[6:8] + line[4:6] + line[2:4] + line[0:2]
        mac = match_mac(line)
        # print(mac)
    fo.close()
    return line


if __name__ == "__main__":
    fo = open(r'./result.log','w')
    mac = aid_to_hex()
    fo.write(mac)
    fo.close()