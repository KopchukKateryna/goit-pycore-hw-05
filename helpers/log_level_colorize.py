from typing import Callable
from colorama import Fore, Style


def get_color(color: str) -> Callable[[str], str]:
    """
    Translates color into code for use by the colorama package.
    Returns a function that applies a color to a string.

    Args:
        * color (str): The color to apply to the string. Default is white

    Returns:
        * Callable[[str], str]: A function that applies the color to a string.
    """
    color_code = getattr(Fore, color.upper(), Fore.WHITE)

    def apply_color(msg: str) -> str:
        """
        Applies a colorama color code to a string.

        Args:
            * msg (str): The string to apply the color to.
        Returns:
            * str: formatted string
        """
        return f"{color_code}{Style.BRIGHT}{msg}{Style.RESET_ALL}"
    return apply_color


log_colors = {
    "INFO": get_color("cyan"),
    "DEBUG": get_color("blue"),
    "ERROR": get_color("red"),
    "WARNING": get_color("yellow"),
    "DEFAULT": get_color("white"),
}


def colorize(key: str) -> Callable[[str], str]:
    """
    Returns a color function based on the log level key.

    This function retrieves the appropriate color formatting function from the log_colors dictionary.
    If the key is not found in the dictionary, it returns the default color function (which applies white color).

    Args:
        key (str): The log level key.

    Returns:
        Callable[[str], str]: A function that applies color formatting to a given message.
    """
    return log_colors.get(key, log_colors['DEFAULT'])


if __name__ == "__main__":
    print(log_colors["INFO"]("This is an info message."))
    print(log_colors["DEBUG"]("This is a debug message."))
    print(log_colors["ERROR"]("This is an error message."))
    print(log_colors["WARNING"]("This is a warning message."))
    print(log_colors["DEFAULT"]("This is a default message."))
