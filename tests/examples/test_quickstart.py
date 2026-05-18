"""PS303 example mirror stub: ensure examples/quickstart.py is syntactically valid."""

import subprocess
import sys
from pathlib import Path

EXAMPLE = Path(__file__).resolve().parents[2] / "examples" / "quickstart.py"


def test_quickstart_example_file_exists_on_disk():
    # Arrange
    path = EXAMPLE

    # Act
    found = path.exists()

    # Assert
    assert found, f"missing example: {path}"


def test_quickstart_example_compiles_without_syntax_errors():
    # Arrange
    path = EXAMPLE

    # Act
    proc = subprocess.run(
        [sys.executable, "-m", "py_compile", str(path)],
        capture_output=True,
        text=True,
    )

    # Assert
    assert proc.returncode == 0, f"py_compile failed:\n{proc.stderr}"
