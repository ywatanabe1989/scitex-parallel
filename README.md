# scitex-parallel

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
