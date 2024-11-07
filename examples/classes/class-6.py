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


def factorial(n: int) -> int:
    """
    Calculates the factorial of a number using recursion.
    
    Args:
        n (int): The number to calculate the factorial of.
    
    Returns:
        int: The factorial of the number.
    """
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)


def count_vowels(text: str) -> int:
    """
    Counts the number of vowels in a string.
    
    Args:
        text (str): The input string.
    
    Returns:
        int: The number of vowels in the string.
    """
    vowels = "aeiou"
    return sum(1 for char in text.lower() if char in vowels)


def reverse_string(text: str) -> str:
    """
    Reverses a given string.
    
    Args:
        text (str): The string to reverse.
    
    Returns:
        str: The reversed string.
    """
    return text[::-1]


def text_analyzer(text: str) -> dict:
    """
    Analyzes a given text by calculating its length, counting vowels, 
    and reversing the text.
    
    Args:
        text (str): The input text.
    
    Returns:
        dict: A dictionary with text analysis results.
    """
    return {
        "length": len(text),
        "vowels": count_vowels(text),
        "reversed": reverse_string(text)
    }


if __name__ == "__main__":
    print(greet_user("Alice"))
    
    print(square_number(5))
    
    print(max_of_two(10, 20))
    
    print(is_even(4))
    print(is_even(7))

    print(factorial(5))
    
    print(count_vowels("Hello World"))
    
    print(reverse_string("Python"))
    
    print(text_analyzer("Hello FastAPI"))
