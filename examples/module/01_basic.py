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
    # Call pypagui after all relevant variables have been initialized and before the action starts
    pypagui.wrap_module(__name__)
    i = 0
    print(f"M={M} ({type(M)})")
    print(f"b={b} ({type(b)})")
    print(f"t={t} ({type(t)})")
