from molio.utils.variables import TERM_SIZE


def print_center(text: str|list[str],
                 emph: bool = False,
                 emph_str: str = "-") -> None:
    """
    A function to print to the center of the terminal.

    Args:
        text (str|list[str]): Text/lines of text to print
        emph (bool, optional): Whether to emphasize the text with a header and footer. Defaults to False.
        emph_str (str, optional): The string to emphasize with. Defaults to "-".
    """
    if emph:
        print("".center(TERM_SIZE, fillchar = emph_str))
    if isinstance(text, str):
        print(text.center(TERM_SIZE))
    elif isinstance(text, list):
        for i in text:
            print(i.center(TERM_SIZE))
    if emph:
        print("".center(TERM_SIZE, fillchar = emph_str))
