#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2025-06-02 16:45:00 (ywatanabe)"
# File: ./tests/scitex_parallel/test__run.py

"""Tests for ``scitex_parallel.run``.

PA-306 / STX-NM002: no ``unittest.mock``, no ``monkeypatch``. The only
collaborator we override in these tests is ``multiprocessing.cpu_count``;
it is swapped at the ``scitex_parallel._run`` module's ``multiprocessing``
attribute via a save/restore context manager so the real
``multiprocessing`` module is never globally mutated.

PA-307: every test carries Arrange / Act / Assert markers, asserts
exactly one fact (TQ007), and has a descriptive name (TQ003).
"""

from __future__ import annotations

import time
import warnings
from contextlib import contextmanager
from typing import Iterator

import pytest

import scitex_parallel._run as _run_mod
from scitex_parallel import run

# ---------------------------------------------------------------------------
# Collaborator swap (test seam — no mocks, no monkeypatch)
# ---------------------------------------------------------------------------


@contextmanager
def _swap_cpu_count(fake_count: int) -> Iterator[None]:
    """Replace ``_run.multiprocessing.cpu_count`` with a fake for the test.

    The production module does ``import multiprocessing`` then calls
    ``multiprocessing.cpu_count()`` — so we save/restore the ``cpu_count``
    attribute on the very ``multiprocessing`` reference that ``_run``
    holds. The module object is shared with the rest of the interpreter,
    therefore we must always restore in ``finally``.
    """
    saved = _run_mod.multiprocessing.cpu_count
    _run_mod.multiprocessing.cpu_count = lambda: fake_count  # type: ignore[assignment]
    try:
        yield
    finally:
        _run_mod.multiprocessing.cpu_count = saved  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# Basic execution
# ---------------------------------------------------------------------------


def test_run_returns_summed_pairs_for_two_arg_callable():
    # Arrange
    def add(x, y):
        return x + y

    args_list = [(1, 4), (2, 5), (3, 6)]

    # Act
    result = run(add, args_list)

    # Assert
    assert result == [5, 7, 9]


def test_run_returns_three_results_for_three_arg_tuples():
    # Arrange
    def add(x, y):
        return x + y

    args_list = [(1, 4), (2, 5), (3, 6)]

    # Act
    result = run(add, args_list)

    # Assert
    assert len(result) == 3


def test_run_returns_squared_values_for_single_argument_callable():
    # Arrange
    def square(x):
        return x * x

    args_list = [(2,), (3,), (4,)]

    # Act
    result = run(square, args_list)

    # Assert
    assert result == [4, 9, 16]


def test_run_returns_products_for_three_argument_callable():
    # Arrange
    def multiply_three(x, y, z):
        return x * y * z

    args_list = [(2, 3, 4), (1, 5, 6), (2, 2, 2)]

    # Act
    result = run(multiply_three, args_list)

    # Assert
    assert result == [24, 30, 8]


# ---------------------------------------------------------------------------
# Tuple-returning callables — transposed result shape
# ---------------------------------------------------------------------------


def test_run_returns_tuple_when_worker_returns_tuple():
    # Arrange
    def divmod_func(x, y):
        return divmod(x, y)

    args_list = [(10, 3), (15, 4), (20, 6)]

    # Act
    result = run(divmod_func, args_list)

    # Assert
    assert isinstance(result, tuple)


def test_run_transposes_tuple_returns_to_two_columns_for_divmod():
    # Arrange
    def divmod_func(x, y):
        return divmod(x, y)

    args_list = [(10, 3), (15, 4), (20, 6)]

    # Act
    result = run(divmod_func, args_list)

    # Assert
    assert len(result) == 2


def test_run_returns_quotients_in_first_column_for_divmod():
    # Arrange
    def divmod_func(x, y):
        return divmod(x, y)

    args_list = [(10, 3), (15, 4), (20, 6)]

    # Act
    result = run(divmod_func, args_list)

    # Assert
    assert result[0] == [3, 3, 3]


def test_run_returns_remainders_in_second_column_for_divmod():
    # Arrange
    def divmod_func(x, y):
        return divmod(x, y)

    args_list = [(10, 3), (15, 4), (20, 6)]

    # Act
    result = run(divmod_func, args_list)

    # Assert
    assert result[1] == [1, 3, 2]


def test_run_transposes_three_element_tuple_returns_to_three_columns():
    # Arrange
    def stats(numbers):
        return sum(numbers), len(numbers), sum(numbers) / len(numbers)

    args_list = [([1, 2, 3],), ([4, 5, 6],), ([7, 8, 9],)]

    # Act
    result = run(stats, args_list)

    # Assert
    assert len(result) == 3


def test_run_returns_sums_in_first_column_for_three_element_tuple():
    # Arrange
    def stats(numbers):
        return sum(numbers), len(numbers), sum(numbers) / len(numbers)

    args_list = [([1, 2, 3],), ([4, 5, 6],), ([7, 8, 9],)]

    # Act
    result = run(stats, args_list)

    # Assert
    assert result[0] == [6, 15, 24]


def test_run_returns_lengths_in_second_column_for_three_element_tuple():
    # Arrange
    def stats(numbers):
        return sum(numbers), len(numbers), sum(numbers) / len(numbers)

    args_list = [([1, 2, 3],), ([4, 5, 6],), ([7, 8, 9],)]

    # Act
    result = run(stats, args_list)

    # Assert
    assert result[1] == [3, 3, 3]


def test_run_returns_averages_in_third_column_for_three_element_tuple():
    # Arrange
    def stats(numbers):
        return sum(numbers), len(numbers), sum(numbers) / len(numbers)

    args_list = [([1, 2, 3],), ([4, 5, 6],), ([7, 8, 9],)]

    # Act
    result = run(stats, args_list)

    # Assert
    assert result[2] == [2.0, 5.0, 8.0]


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------


def test_run_raises_valueerror_when_args_list_is_empty():
    # Arrange
    def dummy(x):
        return x

    # Act
    ctx = pytest.raises(ValueError, match="Args list cannot be empty")

    # Assert
    with ctx:
        run(dummy, [])


def test_run_raises_valueerror_when_func_is_string():
    # Arrange
    args_list = [(1, 2), (3, 4)]

    # Act
    ctx = pytest.raises(ValueError, match="Func must be callable")

    # Assert
    with ctx:
        run("not_callable", args_list)


def test_run_raises_valueerror_when_func_is_integer():
    # Arrange
    args_list = [(1, 2), (3, 4)]

    # Act
    ctx = pytest.raises(ValueError, match="Func must be callable")

    # Assert
    with ctx:
        run(123, args_list)


def test_run_raises_valueerror_when_n_jobs_is_zero():
    # Arrange
    def add(x, y):
        return x + y

    args_list = [(1, 2), (3, 4)]

    # Act
    ctx = pytest.raises(ValueError, match="n_jobs must be >= 1 or -1")

    # Assert
    with ctx:
        run(add, args_list, n_jobs=0)


def test_run_raises_valueerror_when_n_jobs_is_minus_two():
    # Arrange
    def add(x, y):
        return x + y

    args_list = [(1, 2), (3, 4)]

    # Act
    ctx = pytest.raises(ValueError, match="n_jobs must be >= 1 or -1")

    # Assert
    with ctx:
        run(add, args_list, n_jobs=-2)


# ---------------------------------------------------------------------------
# n_jobs handling — exercises the cpu_count seam
# ---------------------------------------------------------------------------


def test_run_returns_correct_results_when_n_jobs_minus_one_uses_all_cpus():
    # Arrange
    def add(x, y):
        return x + y

    args_list = [(1, 2), (3, 4)]

    # Act
    with _swap_cpu_count(4):
        result = run(add, args_list, n_jobs=-1)

    # Assert
    assert result == [3, 7]


def test_run_returns_correct_results_for_explicit_n_jobs_two():
    # Arrange
    def add(x, y):
        return x + y

    args_list = [(1, 2), (3, 4)]

    # Act
    result = run(add, args_list, n_jobs=2)

    # Assert
    assert result == [3, 7]


def test_run_emits_one_warning_when_n_jobs_exceeds_cpu_count():
    # Arrange
    def add(x, y):
        return x + y

    args_list = [(1, 2), (3, 4)]

    # Act
    with _swap_cpu_count(2):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            run(add, args_list, n_jobs=4)

    # Assert
    assert len(w) == 1


def test_run_warning_message_mentions_cpu_count_when_n_jobs_exceeds_cpus():
    # Arrange
    def add(x, y):
        return x + y

    args_list = [(1, 2), (3, 4)]

    # Act
    with _swap_cpu_count(2):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            run(add, args_list, n_jobs=4)

    # Assert
    assert "n_jobs (4) is greater than CPU count (2)" in str(w[0].message)


def test_run_still_returns_correct_results_when_n_jobs_exceeds_cpu_count():
    # Arrange
    def add(x, y):
        return x + y

    args_list = [(1, 2), (3, 4)]

    # Act
    with _swap_cpu_count(2):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            result = run(add, args_list, n_jobs=4)

    # Assert
    assert result == [3, 7]


# ---------------------------------------------------------------------------
# Misc behaviour
# ---------------------------------------------------------------------------


def test_run_accepts_custom_description_and_returns_correct_results():
    # Arrange
    def add(x, y):
        return x + y

    args_list = [(1, 2), (3, 4), (5, 6)]

    # Act
    result = run(add, args_list, desc="Custom Processing")

    # Assert
    assert result == [3, 7, 11]


def test_run_preserves_input_order_despite_variable_completion_times():
    # Arrange
    def delayed_identity(x, delay):
        time.sleep(delay)
        return x

    # Longer delays for smaller numbers to test order preservation
    args_list = [(1, 0.1), (2, 0.05), (3, 0.01)]

    # Act
    result = run(delayed_identity, args_list)

    # Assert
    assert result == [1, 2, 3]


def test_run_propagates_worker_exception_to_caller():
    # Arrange
    def failing_func(x):
        if x == 2:
            raise ValueError(f"Error processing {x}")
        return x * 2

    args_list = [(1,), (2,), (3,)]

    # Act
    ctx = pytest.raises(ValueError, match="Error processing 2")

    # Assert
    with ctx:
        run(failing_func, args_list)


def test_run_returns_dict_results_for_dict_returning_workers():
    # Arrange
    def process_dict(data_dict, multiplier):
        return {k: v * multiplier for k, v in data_dict.items()}

    args_list = [
        ({"a": 1, "b": 2}, 2),
        ({"x": 3, "y": 4}, 3),
        ({"p": 5, "q": 6}, 4),
    ]

    # Act
    result = run(process_dict, args_list)

    # Assert
    assert result == [
        {"a": 2, "b": 4},
        {"x": 9, "y": 12},
        {"p": 20, "q": 24},
    ]


def test_run_returns_factorial_at_index_zero_for_one_indexed_range():
    # Arrange
    def compute_factorial(n):
        if n <= 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    args_list = [(i,) for i in range(1, 11)]

    # Act
    result = run(compute_factorial, args_list)

    # Assert
    assert result[0] == 1  # 1!


def test_run_returns_factorial_at_index_four_for_one_indexed_range():
    # Arrange
    def compute_factorial(n):
        if n <= 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    args_list = [(i,) for i in range(1, 11)]

    # Act
    result = run(compute_factorial, args_list)

    # Assert
    assert result[4] == 120  # 5!


def test_run_returns_factorial_at_index_nine_for_one_indexed_range():
    # Arrange
    def compute_factorial(n):
        if n <= 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    args_list = [(i,) for i in range(1, 11)]

    # Act
    result = run(compute_factorial, args_list)

    # Assert
    assert result[9] == 3628800  # 10!


def test_run_returns_ten_factorials_for_ten_element_args_list():
    # Arrange
    def compute_factorial(n):
        if n <= 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    args_list = [(i,) for i in range(1, 11)]

    # Act
    result = run(compute_factorial, args_list)

    # Assert
    assert len(result) == 10


def test_run_returns_pure_function_results_in_order_for_independent_inputs():
    # Arrange
    def increment_and_return(base, increment):
        # Pure function, no shared state
        return base + increment

    args_list = [(i, 1) for i in range(20)]

    # Act
    result = run(increment_and_return, args_list)

    # Assert
    assert result == list(range(1, 21))


def test_run_returns_lists_in_input_order_for_list_creating_workers():
    # Arrange
    def create_list(size, value):
        return [value] * size

    args_list = [(3, i) for i in range(5)]

    # Act
    result = run(create_list, args_list)

    # Assert
    assert result == [
        [0, 0, 0],
        [1, 1, 1],
        [2, 2, 2],
        [3, 3, 3],
        [4, 4, 4],
    ]


def test_run_returns_formatted_strings_in_input_order():
    # Arrange
    def format_string(template, value):
        return template.format(value)

    args_list = [
        ("Hello {}", "World"),
        ("Number: {}", 42),
        ("Status: {}", "OK"),
    ]

    # Act
    result = run(format_string, args_list)

    # Assert
    assert result == ["Hello World", "Number: 42", "Status: OK"]


if __name__ == "__main__":
    import os

    pytest.main([os.path.abspath(__file__)])

# EOF
