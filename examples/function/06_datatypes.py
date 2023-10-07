import datetime

import pypagui


@pypagui.wrap_function
def f(a: int, b: float, c: bool, d: str, e: datetime.datetime):
    print(f"a={a} ({type(a)})")
    print(f"b={b} ({type(b)})")
    print(f"b={c} ({type(c)})")
    print(f"d={d} ({type(d)})")
    print(f"e={e} ({type(e)})")


if __name__ == '__main__':
    f(7, 3.1415926, True, "abc", datetime.datetime(2023, 9, 17, 17, 15, 2))
