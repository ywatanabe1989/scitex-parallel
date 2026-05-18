"""Smoke test: every example script under examples/ runs to completion.

PA-307: rather than one mega-test that asserts twice (presence + each
script's exit code), we parametrize one example-per-test so a single
failure points at the exact script that broke.
"""

import subprocess
import sys
from pathlib import Path

import pytest

EXAMPLES_DIR = Path(__file__).resolve().parents[2] / "examples"
EXAMPLES = sorted(EXAMPLES_DIR.glob("*.py"))


def test_examples_directory_contains_at_least_one_script():
    # Arrange
    examples = EXAMPLES

    # Act
    count = len(examples)

    # Assert
    assert count >= 1, f"No example scripts found under {EXAMPLES_DIR}"


@pytest.mark.parametrize(
    "example_path",
    EXAMPLES,
    ids=[p.name for p in EXAMPLES] or ["no-examples"],
)
def test_example_script_exits_zero_when_run_directly(example_path, tmp_path):
    # Arrange
    cmd = [sys.executable, str(example_path)]

    # Act
    proc = subprocess.run(
        cmd,
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=120,
    )

    # Assert
    assert proc.returncode == 0, (
        f"{example_path.name} failed:\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
    )
