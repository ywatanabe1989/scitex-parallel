#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ThreadWithReturnValue — a Thread subclass whose join() returns the target's return value.

Ported from scitex-gen ``misc.py``. The upstream version contained a
``NameError`` bug: it called ``Thread.__init__(...)`` and
``Thread.join(...)`` without importing ``Thread``. Fixed here by
qualifying both as :class:`threading.Thread`.
"""
from __future__ import annotations

import threading
from typing import Any, Callable, Optional


class ThreadWithReturnValue(threading.Thread):
    """A :class:`threading.Thread` that returns the target callable's return value via ``join()``.

    Example
    -------
    >>> def square(x):
    ...     return x * x
    >>> t = ThreadWithReturnValue(target=square, args=(7,))
    >>> t.start()
    >>> t.join()
    49
    """

    def __init__(
        self,
        group: None = None,
        target: Optional[Callable[..., Any]] = None,
        name: Optional[str] = None,
        args: tuple = (),
        kwargs: Optional[dict] = None,
        Verbose: Optional[bool] = None,
    ) -> None:
        if kwargs is None:
            kwargs = {}
        # Bug fix: qualify Thread.__init__ as threading.Thread.__init__
        # (the upstream version was a bare `Thread.__init__(...)` with no
        # import, which raised NameError on every construction).
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return: Any = None
        # Verbose kept for backward-compatibility with legacy callers
        # but no longer used.
        self._verbose = Verbose

    def run(self) -> None:
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args, **kwargs) -> Any:
        # Same fix as above — qualify the superclass call.
        threading.Thread.join(self, *args, **kwargs)
        return self._return
