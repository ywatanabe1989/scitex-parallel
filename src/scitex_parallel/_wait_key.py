#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wait_key — block until a key is pressed, then terminate a process.

Unified port of:

- ``scitex_gen._wait_key`` (legacy ``wait_key(process, tgt_key='q')``)
- ``scitex_etc.wait_key.wait_key`` (legacy ``wait_key(p)`` — 'q' hardcoded)

The unified signature is ``wait_key(process, key='q')`` — the ``tgt_key``
kwarg is renamed ``key`` for brevity, and the etc-flavor hardcoded 'q'
becomes the default. Both legacy call shapes (``wait_key(p)`` and
``wait_key(p, 'q')``) keep working.
"""
from __future__ import annotations


def wait_key(process, key: str = "q") -> None:
    """Block until ``key`` is pressed, then terminate ``process``.

    Echoes each pressed key to stdout (matching legacy behavior).
    Requires ``readchar``.

    Parameters
    ----------
    process : multiprocessing.Process or subprocess.Popen
        The process to terminate when ``key`` is pressed. Anything with
        a ``terminate()`` method works.
    key : str, default 'q'
        The keystroke to wait for.

    Example
    -------
    >>> # Inside an interactive script:
    >>> # from scitex_parallel import _return_counting_process, wait_key
    >>> # p = _return_counting_process()
    >>> # wait_key(p)  # press 'q' to stop the counter
    """
    import readchar

    pressed_key = None
    while pressed_key != key:
        pressed_key = readchar.readchar()
        print(pressed_key)
    process.terminate()


def _return_counting_process():
    """Spawn a multiprocessing.Process that prints an incrementing counter.

    Used by the scitex_parallel test suite and as a documentation aid
    for :func:`wait_key`. Private because it's a test helper, not a
    polished public API.
    """
    import multiprocessing
    import time

    def _count() -> None:  # pragma: no cover - runs inside the child process
        counter = 0
        while True:
            print(counter)
            time.sleep(1)
            counter += 1

    p1 = multiprocessing.Process(target=_count)
    p1.start()
    return p1
