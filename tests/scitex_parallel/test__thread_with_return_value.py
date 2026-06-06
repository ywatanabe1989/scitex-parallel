#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for ThreadWithReturnValue."""
from __future__ import annotations

import time

from scitex_parallel import ThreadWithReturnValue


def _square(x):
    return x * x


def _slow_sum(a, b):
    time.sleep(0.05)
    return a + b


class TestThreadWithReturnValue:
    def test_returns_target_result(self):
        t = ThreadWithReturnValue(target=_square, args=(7,))
        t.start()
        assert t.join() == 49

    def test_kwargs(self):
        def add(a, b=0):
            return a + b
        t = ThreadWithReturnValue(target=add, args=(3,), kwargs={"b": 4})
        t.start()
        assert t.join() == 7

    def test_target_none_returns_none(self):
        t = ThreadWithReturnValue()
        t.start()
        assert t.join() is None

    def test_multiple_threads(self):
        threads = [
            ThreadWithReturnValue(target=_slow_sum, args=(i, i + 1))
            for i in range(5)
        ]
        for t in threads:
            t.start()
        results = [t.join() for t in threads]
        assert results == [1, 3, 5, 7, 9]
