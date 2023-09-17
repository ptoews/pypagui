import pypagui


@pypagui.wrap_function
def f(a: int, b: float, c: bool, d: str):
    print(f"{a=} ({type(a)})")
    print(f"{b=} ({type(b)})")
    print(f"{c=} ({type(c)})")
    print(f"{d=} ({type(d)})")


if __name__ == '__main__':
    f(7, 3.1415926, True, "abc")
