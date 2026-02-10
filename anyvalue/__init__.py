"""A better ANY helper for Python testing"""

from anyvalue.any_value import AnyValue

__version__ = "0.0.0"

__all__ = ["AnyValue"]


def add(a: int, b: int) -> int:
    """
    Add two integers.

    Args:
        a:
            The first operand.
        b:
            The second operand.

    Examples:
        Add two integers

            r = add(2, 3)
            print(r)  # 5
    """
    return a + b
