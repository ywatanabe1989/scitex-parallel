#!/usr/bin/env python3
# File: src/scitex_parallel/__init__.py
"""SciTeX Parallel — thread/process pool parallel execution utilities."""

from __future__ import annotations

try:
    from importlib.metadata import version as _v, PackageNotFoundError
    try:
        __version__ = _v("scitex-parallel")
    except PackageNotFoundError:
        __version__ = "0.0.0+local"
    del _v, PackageNotFoundError
except ImportError:  # pragma: no cover — only on ancient Pythons
    __version__ = "0.0.0+local"

from ._run import run

__all__ = [
    "__version__",
    "run",
]

# EOF
