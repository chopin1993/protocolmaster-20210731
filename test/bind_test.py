from functools import partial


def printx(x, y):
    "this is print fun"
    print("x", x)
    print("y",y)


printx(1,2)
print(printx.__doc__)

xx = partial(printx, "1")
print(xx.__doc__)