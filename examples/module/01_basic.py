import sys

import pypagui


M = 3
b = "c"


def x(n: int):
    y = 3
    z = 4
    print(z)
    return y * n


class A:
    aaa = "abc"


if __name__ == '__main__':
    t = 111
    pypagui.wrap_module(sys.modules[__name__])
