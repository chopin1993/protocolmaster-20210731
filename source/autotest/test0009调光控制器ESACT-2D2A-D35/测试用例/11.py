# coding:utf-8
# 计算分数20210415-test


def handle():
    average = 83
    total = average * 3
    for c in range(0, 10):
        for m in range(1, 10):
            chinese1 = int('9' + str(c))
            print('chinese total:', int(chinese1))
            math1 = int(str(m) + '9')
            print('math total:', int(math1))
            while total == chinese1 + math1 + 95:
                chinese = chinese1
                math = math1
                break

    return chinese, math


print('chinese-total & math-total :', handle())
