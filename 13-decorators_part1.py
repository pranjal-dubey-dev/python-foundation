"""The object-oriented Decorator design pattern.

The pattern adds behavior to an object without changing the wrapped object's
class. Each decorator implements the same interface as the component it wraps.
"""

import logging
from abc import ABC, abstractmethod
from math import sqrt
from time import perf_counter


logger = logging.getLogger(__name__)


def is_prime(number: int) -> bool:
    """Return whether *number* is prime."""
    if number < 2:
        return False

    for divisor in range(2, int(sqrt(number)) + 1):
        if number % divisor == 0:
            return False
    return True


class AbstractComponent(ABC):
    """Interface shared by the component and its decorators."""

    @abstractmethod
    def execute(self, upper_bound: int) -> int:
        """Count or otherwise process values below *upper_bound*."""


class ConcreteComponent(AbstractComponent):
    """The original object whose behavior will be decorated."""

    def execute(self, upper_bound: int) -> int:
        return sum(is_prime(number) for number in range(upper_bound))


class AbstractDecorator(AbstractComponent):
    """Base class for decorators that delegate to another component."""

    def __init__(self, decorated: AbstractComponent) -> None:
        self._decorated = decorated


class LoggingDecorator(AbstractDecorator):
    """Log before and after delegating execution."""

    def execute(self, upper_bound: int) -> int:
        logger.info("Starting execution")
        value = self._decorated.execute(upper_bound)
        logger.info("Execution completed")
        return value


class BenchmarkDecorator(AbstractDecorator):
    """Measure how long the wrapped component takes to execute."""

    def execute(self, upper_bound: int) -> int:
        start_time = perf_counter()
        value = self._decorated.execute(upper_bound)
        run_time = perf_counter() - start_time
        logger.info(
            "Execution of %s took %.2f seconds",
            self._decorated.__class__.__name__,
            run_time,
        )
        return value


def main() -> None:
    """Run the decorators in a chain around the concrete component."""
    logging.basicConfig(level=logging.INFO)

    component = ConcreteComponent()
    component_with_logging = LoggingDecorator(component)
    decorated_component = BenchmarkDecorator(component_with_logging)

    value = decorated_component.execute(100_000)
    logger.info("Found %d primes.", value)


if __name__ == "__main__":
    main()
