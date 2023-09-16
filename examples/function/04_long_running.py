import time

import pypagui


@pypagui.wrap_function
def main(start: int):
    for i in reversed(range(start)):
        print(f"T-{i}")
        time.sleep(1)


if __name__ == '__main__':
    main(5)
