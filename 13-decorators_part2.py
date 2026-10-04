"""Function decorators: function objects, closures, and wrappers.

This lesson builds a decorator from the underlying concepts before showing
decorators that accept arbitrary arguments and handle exceptions.
"""

import functools
import logging
from collections.abc import Callable
from typing import Any


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Function objects and higher-order functions
# ---------------------------------------------------------------------------

def square(value: int) -> int:
    """Return the square of *value*."""
    return value**2


def my_map(function: Callable[[int], int], values: list[int]) -> list[int]:
    """Apply *function* to every item in *values*."""
    return [function(value) for value in values]


# ---------------------------------------------------------------------------
# Closures
# ---------------------------------------------------------------------------

def logger_factory(message: str) -> Callable[[], None]:
    """Return a function that remembers *message*."""
    def log_message() -> None:
        print("Log:", message)

    return log_message


def html_tag(tag: str) -> Callable[[str], None]:
    """Return a function that prints text wrapped in *tag*."""
    def wrap_text(message: str) -> None:
        print(f"<{tag}>{message}</{tag}>")

    return wrap_text


def outer_function(message: str) -> Callable[[], None]:
    """Return a function that remembers its enclosing message."""
    def inner_function() -> None:
        print(message)

    return inner_function


# ---------------------------------------------------------------------------
# Building decorators
# ---------------------------------------------------------------------------

def decorator_function(function: Callable[[], None]) -> Callable[[], None]:
    """Add messages before and after a no-argument function."""
    @functools.wraps(function)
    def wrapper() -> None:
        print("Before")
        function()
        print("After")

    return wrapper


def greet(function: Callable[..., Any]) -> Callable[..., Any]:
    """Print a greeting around a function call."""
    @functools.wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print("Greetings!")
        result = function(*args, **kwargs)
        print("Thanks for using this function")
        return result

    return wrapper


@greet
def hello() -> None:
    print("Hello World")


@greet
def add(first: int, second: int) -> None:
    print(first + second)


def log_function_call(function: Callable[..., Any]) -> Callable[..., Any]:
    """Log a function's name, arguments, and return value."""
    @functools.wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.info(
            "Calling %s with args=%s, kwargs=%s",
            function.__name__,
            args,
            kwargs,
        )
        result = function(*args, **kwargs)
        logger.info("%s returned %s", function.__name__, result)
        return result

    return wrapper


def log_errors(function: Callable[..., Any]) -> Callable[..., Any]:
    """Log exceptions and re-raise them without hiding the failure."""
    @functools.wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return function(*args, **kwargs)
        except Exception:
            logger.exception("Error occurred in %s", function.__name__)
            raise

    return wrapper


@log_function_call
def multiply(first: int, second: int) -> int:
    return first * second


@log_errors
def divide(first: float, second: float) -> float:
    return first / second


def main() -> None:
    """Run the examples in the order they are introduced."""
    logging.basicConfig(level=logging.INFO)

    function = square
    print(function(5))
    print(my_map(square, [1, 2, 3, 4, 5]))

    logger_factory("Hi!")()
    print_h1 = html_tag("h1")
    print_h1("Test Headline!")

    outer_function("Hi")()
    outer_function("Bye")()

    decorated_display = decorator_function(
        lambda: print("Display function ran.")
    )
    decorated_display()
    hello()
    add(1, 2)

    multiply(3, 4)
    try:
        divide(10, 0)
    except ZeroDivisionError:
        logger.info("The expected division error was re-raised.")


if __name__ == "__main__":
    main()
