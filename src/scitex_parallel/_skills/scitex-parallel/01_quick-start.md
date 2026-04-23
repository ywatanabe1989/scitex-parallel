<!-- 01_quick-start.md -->

# scitex-parallel — Quick Start

## Install

```bash
pip install scitex-parallel
```

## Import

```python
from scitex_parallel import run
```

## Run a function over many argument tuples

```python
from scitex_parallel import run

def add(x, y):
    return x + y

args_list = [(1, 4), (2, 5), (3, 6)]
results = run(add, args_list, n_jobs=-1, desc="adding")
# results == [5, 7, 9]  (order preserved)
```

## Public API

`scitex_parallel.__all__` contains one symbol:

| Symbol | Kind | One-liner |
|--------|------|-----------|
| `run` | function | Thread-pool parallel map with tqdm progress bar. |

## Signature

```python
run(
    func: Callable,
    args_list: List[tuple],
    n_jobs: int = -1,          # -1 uses all CPU cores
    desc: str = "Processing",  # tqdm description
) -> List[Any]
```

Each entry of `args_list` is unpacked as `func(*entry)`. For keyword-only
calls, wrap `func` in a small adapter. For CPU-bound work prefer
`multiprocessing` or `joblib` — this helper uses threads and is
GIL-limited.
