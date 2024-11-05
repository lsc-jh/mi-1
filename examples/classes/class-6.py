# Copyright (c) 2024 Joshua Hegedys. All Rights Reserved.

def greet_user(name: str) -> str:
    """
    Greets the user with their name.

    Args:
        name (str): The name of the user.

    Returns:
        str: A greeting message.
    """
    return f"Hello, {name}!"


def square_number(number: int) -> int:
    """
    Calculates the square of a given number.
    
    Args:
        number (int): The number to be squared.
    
    Returns:
        int: The square of the number.
    """
    return number ** 2


def max_of_two(a: int, b: int) -> int:
    """
    Returns the larger of two numbers.
    
    Args:
        a (int): The first number.
        b (int): The second number.
    
    Returns:
        int: The larger of the two numbers.
    """
    return max(a, b)


def is_even(number: int) -> bool:
    """
    Checks if a number is even.
    
    Args:
        number (int): The number to check.
    
    Returns:
        bool: True if the number is even, False otherwise.
    """
    return number % 2 == 0


def calculator(a: float, b: float, operator: str) -> float | None:
    """
    Performs a calculation based on the given operator.
    
    Args:
        a (float): The first number.
        b (float): The second number.
        operator (str): The operator (+, -, *, /).
    
    Returns:
        float: The result of the calculation.
    """
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return a / b
    else:
        return None
