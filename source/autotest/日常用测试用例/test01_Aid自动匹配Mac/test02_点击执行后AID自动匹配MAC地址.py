# encoding = "UTF-8"
"""
1、AID转16进制，并且小端倒置
2、匹配函数
3、输出结果至txt中
"""


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
            logger.debug("经过转换后的16进制小端显示： {0}".format(line))
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
    # logger.debug("16转换成10进制后为：{}".format(aid))
    return aid


def match_mac(aid):
    """
    在监控器搜索MAC地址的列表中，查询当期的aid匹配的mac，并输出
    :param aid:输入aid信息
    """
    import os
    file_list = os.listdir()
    logger.debug("当前目录文件路径path： {0}".format(file_list))
    for i in file_list:
        if "ROUTEREXPORT" in i:
            path = i
            break
    logger.debug("查询Mac地址文件路径path： {0}".format(path))

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
    logger.debug("aid= {0} 对应的mac地址：{1} ".format(aid, mac))
    fo.close()
    return mac


if __name__ == "__main__":
    import logging
    # 添加日志打印模块
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    logger.info("Start print log")

    result_file = open(r'匹配结果.txt', 'w+', encoding="UTF-8")
    device_list = aid_to_hex()
    if len(device_list) == 0:
        result_file.write("未发现有效的AID")
    else:
        for i in device_list:
            result_file.write(match_mac(i) + "    0000    " + hex_to_aid(i) + "\n")
    result_file.close()

    logger.info("Finish print log")
