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

<p align="center">
  <a href="https://scitex.ai">
    <img src="docs/scitex-logo-blue-cropped.png" alt="SciTeX" width="400">
  </a>
</p>

<p align="center"><b>Thread/process pool parallel execution utilities — `map` with tqdm, auto CPU count.</b></p>

<p align="center">
  <a href="https://scitex-parallel.readthedocs.io/">Full Documentation</a> · <code>pip install scitex-parallel</code>
</p>

---

## Problem and Solution

| # | Problem | Solution |
|---|---------|----------|
| 1 | **`concurrent.futures` is low-level** — users rewrite "map-with-progress-bar" every project | **`stx.parallel.run(func, args)`** — drop-in `map` with tqdm, auto CPU-count; 1-liner for I/O-bound workloads (HTTP, file reads, API calls) |
| 2 | **`joblib.Parallel` is heavyweight + process-based by default** — overkill for threaded I/O | **Thread-based, no dep beyond stdlib + tqdm** — right tool for the 80% case |

## Installation

```bash
pip install scitex-parallel
```

## Quick Start

```python
from scitex_parallel import run

results = run(my_func, items, n_jobs=4)
```

## 1 Interfaces

<details open>
<summary><strong>Python API</strong></summary>

<br>

```python
from scitex_parallel import run

# I/O-bound parallel map with tqdm progress bar.
results = run(fetch_url, urls, n_jobs=8, desc="Fetching")

# Tuple-arg form for multi-arg functions.
results = run(my_func, [(a, b) for a, b in zip(xs, ys)], n_jobs=4)
```

</details>

## Part of SciTeX

`scitex-parallel` is part of [**SciTeX**](https://scitex.ai). Install via
the umbrella with `pip install scitex[parallel]` to use as
`scitex.parallel` (Python) or `scitex parallel ...` (CLI).

>Four Freedoms for Research
>
>0. The freedom to **run** your research anywhere — your machine, your terms.
>1. The freedom to **study** how every step works — from raw data to final manuscript.
>2. The freedom to **redistribute** your workflows, not just your papers.
>3. The freedom to **modify** any module and share improvements with the community.
>
>AGPL-3.0 — because we believe research infrastructure deserves the same freedoms as the software it runs on.

## License

AGPL-3.0

---

<p align="center">
  <a href="https://scitex.ai" target="_blank"><img src="docs/scitex-icon-navy-inverted.png" alt="SciTeX" width="40"/></a>
</p>
