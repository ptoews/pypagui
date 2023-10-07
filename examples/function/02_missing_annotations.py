"""
Missing annotations is currently not supported. It is planned to add datatype dropdowns to the GUI,
which would then allow specifying the type at runtime thus allowing missing annotations.
"""
import pypagui


@pypagui.wrap_function
def main(text, offset):
    print(text[offset:])


if __name__ == '__main__':
    main("Hello ", 2)
