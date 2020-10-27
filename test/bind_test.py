from functools import partial


def printx(x, y):
    "this is print fun"
    print("x", x)
    print("y",y)


printx(1,2)
print(printx.__doc__)

xx = partial(printx, "1")
print(xx.__doc__)

print("--------------------------")

def xxx_test():
    """
    第一句
    详细名称
    group: 111111111
    dafad
    case:222222222222222
    123432423
    """
    pass

print(xxx_test.__doc__)

print("--------------------------")
import re
str1 = xxx_test.__doc__
search = re.search(r"group:(.*)case:(.*)",str1,re.S)
print(search.group(1).strip(), search.group(2).strip())