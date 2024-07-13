"""
Реалізуйте функцію caching_fibonacci, яка створює та використовує кеш для зберігання 
і повторного використання вже обчислених значень чисел Фібоначчі.
"""

from typing import Callable


def caching_fibonacci() -> Callable[[int], int]:
    """
    A function that creates and uses a cache to store
    and reuse of already calculated values of Fibonacci numbers

    Args:
        * None

    Returns:
        * fibonacci(function): A Fibonacci function
    """
    cache: dict[int, int] = {}

    def fibonacci(n: int) -> int:
        """
        Computes the nth Fibonacci number using recursion and caching.

        Args:
            * n(int): The position in the Fibonacci sequence to compute.

        Returns:
            * int: The nth Fibonacci number.
        """
        if n < 0:
            raise ValueError("Input must be a positive integer.")
        if n in cache:
            return cache[n]
        if n <= 1:
            return n
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


fib = caching_fibonacci()

print(fib(10))  # Виведе 55
print(fib(15))  # Виведе 610
print(fib(20))  # Виведе 6765
print(fib(30))  # Виведе 832040
print(fib(0))  # Виведе 832040
print(fib(-7))  # Виведе 832040
