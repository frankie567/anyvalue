# AnyValue

<p align="center">
    <em>A better ANY helper for Python testing</em>
</p>

[![build](https://github.com/frankie567/anyvalue/workflows/Build/badge.svg)](https://github.com/frankie567/anyvalue/actions)
[![codecov](https://codecov.io/gh/frankie567/anyvalue/branch/master/graph/badge.svg)](https://codecov.io/gh/frankie567/anyvalue)
[![PyPI version](https://badge.fury.io/py/anyvalue.svg)](https://badge.fury.io/py/anyvalue)

---

**Documentation**: <a href="https://frankie567.github.io/anyvalue/" target="_blank">https://frankie567.github.io/anyvalue/</a>

**Source Code**: <a href="https://github.com/frankie567/anyvalue" target="_blank">https://github.com/frankie567/anyvalue</a>

---

## QuickStart

A smarter alternative to `unittest.mock.ANY` that allows type checking and validation constraints.

### Installation

```bash
pip install anyvalue
```

```bash
uv add anyvalue
```

### Basic Usage

```python
from anyvalue import AnyValue
from annotated_types import Ge, Le, Len, Predicate
from datetime import datetime
from unittest.mock import Mock

# Basic type matching
assert 42 == AnyValue(int)
assert "hello" == AnyValue(str)
assert datetime.now() == AnyValue(datetime)

# Multiple types with union operator
assert 42 == AnyValue(int | float)
assert "test" == AnyValue(str | bytes)

# None support
assert None == AnyValue(None)
assert None == AnyValue(str | None)
assert 42 == AnyValue(int | None)

# Validation constraints
assert 42 == AnyValue(int, Ge(0))  # Non-negative integer
assert "hello" == AnyValue(str, Len(5, 5))  # String of length 5
assert 99 == AnyValue(int, Ge(0), Le(100))  # Integer between 0 and 100

# Predicate validators
is_even = Predicate(lambda x: x % 2 == 0)
assert 42 == AnyValue(int, is_even)

# Custom callable validators
def is_palindrome(s: str) -> bool:
    return s == s[::-1]

assert "racecar" == AnyValue(str, is_palindrome)

# Integration with unittest.mock
mock_func = Mock()
mock_func(42, "test", datetime.now())

# Verify calls with flexible matching
mock_func.assert_called_once_with(
    AnyValue(int, Ge(0)),
    AnyValue(str, Len(4, 10)),
    AnyValue(datetime)
)
```

### Key Features

- **Type checking**: Accept specific types or union of types
- **None support**: Explicitly allow or disallow None values
- **Validation constraints**: Use `annotated-types` for advanced validation (length, ranges, patterns, etc.)
- **Mock integration**: Works seamlessly with `unittest.mock` for validating call arguments

---

## Development

### Setup environment

We use [uv](https://docs.astral.sh/uv/) to manage the development environment and production build, and [just](https://github.com/casey/just) to manage command shortcuts. Ensure they are installed on your system.

### Run unit tests

You can run all the tests with:

```bash
just test
```

### Format the code

Execute the following command to apply linting and check typing:

```bash
just lint
```

### Publish a new version

You can bump the version, create a commit and associated tag with one command:

```bash
just version patch
```

```bash
just version minor
```

```bash
just version major
```

Your default Git text editor will open so you can add information about the release.

When you push the tag on GitHub, the workflow will automatically publish it on PyPi and a GitHub release will be created as draft.

## Serve the documentation

You can serve the Mkdocs documentation with:

```bash
just docs-serve
```

It'll automatically watch for changes in your code.

## License

This project is licensed under the terms of the MIT license.
