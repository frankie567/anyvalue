# AnyValue Guide

## Overview

`AnyValue` is a powerful matcher for Python testing that extends the functionality of `unittest.mock.ANY` by supporting type checking and validation constraints. It's perfect for situations where you need to verify that a value meets certain criteria without checking the exact value.

## Problem Statement

In standard `unittest.mock`, the `ANY` matcher equals any value, which is useful but too permissive. Sometimes you need to verify that a value is of a specific type or meets certain constraints without checking the exact value.

For example, when testing a function that creates a user:

```python
# Too permissive
mock_api.create_user.assert_called_once_with(ANY, ANY, ANY, ANY)

# Too strict - requires exact values
mock_api.create_user.assert_called_once_with(12345, "john_doe", "john@example.com", 25)
```

## Solution

`AnyValue` provides a middle ground, allowing you to specify type and validation constraints:

```python
from anyvalue import AnyValue
from annotated_types import Ge, Le, Len

mock_api.create_user.assert_called_once_with(
    user_id=AnyValue(int, Ge(1)),           # Positive user ID
    username=AnyValue(str, Len(1, 50)),     # Username between 1-50 chars
    email=AnyValue(str),                    # Any string email
    age=AnyValue(int, Ge(0), Le(150))       # Age between 0-150
)
```

## Features

### Type Checking

Match specific types or union of types:

```python
from anyvalue import AnyValue
from datetime import datetime

# Single type
assert 42 == AnyValue(int)
assert "hello" == AnyValue(str)
assert datetime.now() == AnyValue(datetime)

# Union types using | operator
assert 42 == AnyValue(int | float)
assert 3.14 == AnyValue(int | float)
assert "test" == AnyValue(str | bytes)
assert b"test" == AnyValue(str | bytes)
```

### None Support

Explicitly allow or disallow None values:

```python
from anyvalue import AnyValue

# None type explicitly
assert None == AnyValue(None)

# None in union
assert None == AnyValue(str | None)
assert None == AnyValue(int | None)
assert 42 == AnyValue(int | None)  # Actual values still work

# None not allowed when not specified
assert not (None == AnyValue(int))
```

### Validation Constraints

Use `annotated-types` for advanced validation:

```python
from anyvalue import AnyValue
from annotated_types import Ge, Le, Gt, Lt, Len, MultipleOf

# Greater than or equal (>=)
assert 42 == AnyValue(int, Ge(0))  # Non-negative integer
assert 100 == AnyValue(int, Ge(0))
assert not (-1 == AnyValue(int, Ge(0)))

# Less than or equal (<=)
assert 50 == AnyValue(int, Le(100))
assert not (101 == AnyValue(int, Le(100)))

# Range constraints
assert 50 == AnyValue(int, Ge(0), Le(100))  # Between 0 and 100
assert not (-1 == AnyValue(int, Ge(0), Le(100)))
assert not (101 == AnyValue(int, Ge(0), Le(100)))

# Length constraints
assert "hello" == AnyValue(str, Len(5, 5))  # Exact length 5
assert "test" == AnyValue(str, Len(1, 10))  # Length between 1 and 10
assert [1, 2, 3] == AnyValue(list, Len(3, 3))  # List of length 3

# Multiple of
assert 10 == AnyValue(int, MultipleOf(5))
assert not (11 == AnyValue(int, MultipleOf(5)))
```

### Predicate Validators

Use `Predicate` for custom validation logic:

```python
from anyvalue import AnyValue
from annotated_types import Predicate

# Even numbers
is_even = Predicate(lambda x: x % 2 == 0)
assert 42 == AnyValue(int, is_even)
assert not (43 == AnyValue(int, is_even))

# Positive numbers
is_positive = Predicate(lambda x: x > 0)
assert 100 == AnyValue(int, is_positive)
assert not (0 == AnyValue(int, is_positive))

# String patterns
starts_with_hello = Predicate(lambda x: x.startswith("hello"))
assert "hello world" == AnyValue(str, starts_with_hello)
assert not ("goodbye" == AnyValue(str, starts_with_hello))

# Combine with other constraints
assert 42 == AnyValue(int, Ge(0), is_even)
```

### Custom Callable Validators

Use any callable function as a validator:

```python
from anyvalue import AnyValue

# Palindrome checker
def is_palindrome(s: str) -> bool:
    return s == s[::-1]

assert "racecar" == AnyValue(str, is_palindrome)
assert "level" == AnyValue(str, is_palindrome)
assert not ("hello" == AnyValue(str, is_palindrome))

# Prime number checker
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

assert 7 == AnyValue(int, is_prime)
assert 13 == AnyValue(int, is_prime)
assert not (4 == AnyValue(int, is_prime))

# Combine with annotated-types constraints
assert 7 == AnyValue(int, Ge(0), is_prime)
```

## Mock Integration

`AnyValue` works seamlessly with `unittest.mock`:

```python
from anyvalue import AnyValue
from annotated_types import Ge, Le, Len, Predicate
from datetime import datetime
from unittest.mock import Mock

# Create a mock function
mock_func = Mock()

# Call it with some values
mock_func(42, "test", datetime.now())

# Verify with AnyValue matchers
mock_func.assert_called_once_with(
    AnyValue(int),
    AnyValue(str),
    AnyValue(datetime)
)

# Test with constraints
mock_func.reset_mock()
mock_func(100, "hello")

mock_func.assert_called_once_with(
    AnyValue(int, Ge(0), Le(1000)),
    AnyValue(str, Len(5, 5))
)

# Test with union types and None
mock_func.reset_mock()
mock_func(None, "test")

mock_func.assert_called_once_with(
    AnyValue(int | None),
    AnyValue(str)
)
```

## Real-World Examples

### API Response Validation

```python
from anyvalue import AnyValue
from annotated_types import Ge, Le, Len
from unittest.mock import Mock

mock_api = Mock()
mock_api.create_user(
    user_id=12345,
    username="john_doe",
    email="john@example.com",
    age=25
)

mock_api.create_user.assert_called_once_with(
    user_id=AnyValue(int, Ge(1)),           # Positive user ID
    username=AnyValue(str, Len(1, 50)),     # Username between 1-50 chars
    email=AnyValue(str),                    # Any string email
    age=AnyValue(int, Ge(0), Le(150))       # Age between 0-150
)
```

### Optional Parameters

```python
from anyvalue import AnyValue
from datetime import datetime
from unittest.mock import Mock

mock_service = Mock()
mock_service.process(data="test", timestamp=datetime.now(), metadata=None)

mock_service.process.assert_called_once_with(
    data=AnyValue(str),
    timestamp=AnyValue(datetime),
    metadata=AnyValue(dict | None)  # Optional metadata
)
```

### Email Validation

```python
from anyvalue import AnyValue
from annotated_types import Predicate
from unittest.mock import Mock

is_valid_email = Predicate(lambda x: "@" in x and "." in x)

mock_validator = Mock()
mock_validator.send_email("user@example.com")

mock_validator.send_email.assert_called_once_with(
    AnyValue(str, is_valid_email)
)
```

## Error Messages

`AnyValue` provides descriptive error messages when assertions fail:

```python
from anyvalue import AnyValue
from annotated_types import Ge

# Type mismatch
matcher = AnyValue(int)
result = matcher == "hello"
# Error: Expected type int, got str ('hello')

# Validator failure
matcher = AnyValue(int, Ge(10))
result = matcher == 5
# Error: Validator Ge(ge=10) failed: 5 is not >= 10

# Length validator
matcher = AnyValue(str, Len(5, 5))
result = matcher == "hi"
# Error: Validator Len(min_length=5, max_length=5) failed: length 2 is less than min 5
```

## Design Decisions

- **Class-based approach**: Instantiate with parameters rather than a global constant
- **Type-first API**: The first argument is always the type constraint
- **Union support**: Use Python's `|` operator for multiple types
- **Explicit None**: None must be explicitly included in the type union
- **annotated-types integration**: Leverage existing validation library for constraints
- **Hard dependency**: annotated-types is a required dependency (not optional)

## API Reference

For detailed API documentation, see the [Reference](reference/anyvalue/any_value.md) section.
