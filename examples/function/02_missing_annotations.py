import pypagui


@pypagui.wrap_function
def main(text, offset):
    print(text[offset:])


if __name__ == '__main__':
    main("Hello ", 2)
