from molio.utils.variables import TERM_SIZE


def print_center(text: str|list[str], emph: bool = False) -> None:
    if emph:
        print("".center(TERM_SIZE, fillchar = "-"))
    if isinstance(text, str):
        print(text.center(TERM_SIZE))
    elif isinstance(text, list):
        for i in text:
            print(i.center(TERM_SIZE))
    if emph:
        print("".center(TERM_SIZE, fillchar = "-"))
