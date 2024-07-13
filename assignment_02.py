"""
Cтворити функцію generator_numbers, яка буде аналізувати текст, ідентифікувати всі
дійсні числа, що вважаються частинами доходів, і повертати їх як генератор. Дійсні
числа у тексті записані без помилок, чітко відокремлені пробілами з обох боків.
Також потрібно реалізувати функцію sum_profit, яка буде використовувати 
generator_numbers для підсумовування цих чисел і обчислення загального прибутку.
"""

import re
from decimal import Decimal
from typing import Callable, Generator

FLOAT_NUMBER_PATTERN = r"\b-?\d+(?:\.\d+)?\b"


def generator_numbers(input_text: str) -> Generator[Decimal, None, None]:
    """
    A function that takes a string as an argument and returns a generator that iterates
    over all found real numbers in the text that are delimited by spaces using regex.

    Args:
        * text (str): The text to be analyzed.
    
    Returns:
        * Generator[float, None, None]: A generator that iterates over all found real numbers.
    """
    for match in re.findall(FLOAT_NUMBER_PATTERN, input_text):
        yield Decimal(match)


def sum_profit(input_text: str, func: Callable):
    """
    A function that uses the generator generator_numbers to calculate the total sum of
    the numbers in the input string and takes the function as an argument when called.

    Args:
        * text (str): The text to be analyzed.
        * func (Callable[[str], Generator[Decimal, None, None]]): The generator function that iterates over numbers in the text.

    Returns:
        * float: The total sum of the numbers.
    """
    numbers = [number.quantize(Decimal("0.00")) for number in func(input_text)]
    return float(sum(numbers))

    # return float(sum(func(text))) and it could have been like this, just 1 line =))


text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income}")  # Загальний дохід: 1351.46
