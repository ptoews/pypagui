import pypagui


@pypagui.wrap_function
def main(text: str, count: int):
    print(text * count)


if __name__ == '__main__':
    main("Hello ", 5)
