# scitex-parallel

<!-- scitex-badges:start -->
[![PyPI](https://img.shields.io/pypi/v/scitex-parallel.svg)](https://pypi.org/project/scitex-parallel/)
[![Python](https://img.shields.io/pypi/pyversions/scitex-parallel.svg)](https://pypi.org/project/scitex-parallel/)
[![Tests](https://github.com/ywatanabe1989/scitex-parallel/actions/workflows/test.yml/badge.svg)](https://github.com/ywatanabe1989/scitex-parallel/actions/workflows/test.yml)
[![Install Test](https://github.com/ywatanabe1989/scitex-parallel/actions/workflows/install-test.yml/badge.svg)](https://github.com/ywatanabe1989/scitex-parallel/actions/workflows/install-test.yml)
[![Coverage](https://codecov.io/gh/ywatanabe1989/scitex-parallel/graph/badge.svg)](https://codecov.io/gh/ywatanabe1989/scitex-parallel)
[![Docs](https://readthedocs.org/projects/scitex-parallel/badge/?version=latest)](https://scitex-parallel.readthedocs.io/en/latest/)
[![License: AGPL v3](https://img.shields.io/badge/license-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
<!-- scitex-badges:end -->


Thread/process pool parallel execution utilities for the SciTeX ecosystem.

## Problem and Solution


| # | Problem | Solution |
|---|---------|----------|
| 1 | **`concurrent.futures` is low-level** -- users rewrite "map-with-progress-bar" every project | **`stx.parallel.run(func, args)`** -- drop-in `map` with tqdm, auto CPU-count; 1-liner for I/O-bound workloads (HTTP, file reads, API calls) |
| 2 | **`joblib.Parallel` is heavyweight + process-based by default** -- overkill for threaded I/O | **Thread-based, no dep beyond stdlib + tqdm** -- right tool for the 80% case |

## Installation

```bash
pip install scitex-parallel
```

## Usage

```python
from scitex_parallel import run

results = run(my_func, items, n_jobs=4)
```

## License

AGPL-3.0
