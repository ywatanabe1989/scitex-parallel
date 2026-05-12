"""Pytest fixtures and rootdir marker for this package.

An empty conftest.py at tests/ is the canonical SciTeX
convention (audit-project PS208) — it pins the pytest
rootdir and gives downstream fixtures a home.

Also wires subprocess coverage: tests that spawn a child Python
interpreter (subprocess.run, jupyter nbconvert --execute, etc.)
would otherwise drop their coverage data because pytest-cov sets
COVERAGE_FILE to a per-test tmp dir before conftest.py runs.

The three pieces of the wiring:

1. `[tool.coverage.run] parallel=true` in pyproject.toml (every
   process writes to its own `.coverage.<host>.<pid>` shard).
2. Force-set (NOT setdefault — that's a silent no-op since pytest-cov
   has already populated the env var) COVERAGE_PROCESS_START and
   COVERAGE_FILE at module-import time, before any test code runs.
3. Drop an idempotent `.pth` file in site-packages so child Python
   interpreters call `coverage.process_startup()` during site init.

See the `05_development_06_subprocess-coverage.md` skill leaf.
"""

from __future__ import annotations

import os
import sysconfig
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Pin coverage's data file at the repo root and point process_startup
# at our pyproject so child interpreters configure themselves correctly.
os.environ["COVERAGE_PROCESS_START"] = str(_PROJECT_ROOT / "pyproject.toml")
os.environ["COVERAGE_FILE"] = str(_PROJECT_ROOT / ".coverage")


def _ensure_subprocess_coverage_shim() -> None:
    """Drop an idempotent `.pth` file in site-packages that auto-starts
    coverage in every child Python interpreter via
    `coverage.process_startup()`.
    """
    purelib = Path(sysconfig.get_paths()["purelib"])
    pth = purelib / "_scitex_parallel_subprocess_coverage.pth"
    shim = (
        "import os, coverage\n"
        "if os.environ.get('COVERAGE_PROCESS_START'):\n"
        "    coverage.process_startup()\n"
    )
    try:
        if not pth.exists() or pth.read_text() != shim:
            pth.write_text(shim)
    except OSError:
        # site-packages may be read-only (e.g. system Python); silently
        # skip — local dev venvs are writable and that's where this matters.
        pass


_ensure_subprocess_coverage_shim()
