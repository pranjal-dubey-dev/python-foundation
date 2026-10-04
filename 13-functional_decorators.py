"""Reusable function decorators composed around a prime-counting function."""

import functools
import logging
from collections.abc import Callable
from math import sqrt
from time import perf_counter
from typing import Any


logger = logging.getLogger(__name__)


def is_prime(number: int) -> bool:
    """Return whether *number* is prime."""
    if number < 2:
        return False

    for divisor in range(2, int(sqrt(number)) + 1):
        if number % divisor == 0:
            return False
    return True


def benchmark(function: Callable[..., Any]) -> Callable[..., Any]:
    """Log the execution time of *function*."""
    @functools.wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter()
        value = function(*args, **kwargs)
        run_time = perf_counter() - start_time
        logger.info(
            "Execution of %s took %.2f seconds",
            function.__name__,
            run_time,
        )
        return value

    return wrapper


def with_logging(
    function: Callable[..., Any],
    *,
    logger: logging.Logger,
) -> Callable[..., Any]:
    """Log when *function* starts and finishes."""
    @functools.wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.info("Calling %s", function.__name__)
        value = function(*args, **kwargs)
        logger.info("Finished calling %s", function.__name__)
        return value

    return wrapper


with_default_logging = functools.partial(with_logging, logger=logger)


@with_default_logging
@benchmark
def count_primes(upper_bound: int) -> int:
    """Count prime numbers below *upper_bound*."""
    return sum(is_prime(number) for number in range(upper_bound))


def main() -> None:
    """Run the composed decorators."""
    logging.basicConfig(level=logging.INFO)
    value = count_primes(100_000)
    logger.info("Found %d primes.", value)


if __name__ == "__main__":
    main()
