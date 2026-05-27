---
description: |
  [TOPIC] scitex-parallel Python API
  [DETAILS] One public callable — run() maps func over arg tuples on a ThreadPoolExecutor with tqdm.
tags: [scitex-parallel-python-api]
---

# Python API

`scitex_parallel.__all__` contains two symbols.

## Public symbols

| Name          | Kind     | Purpose                                              |
|---------------|----------|------------------------------------------------------|
| `__version__` | str      | Installed package version                            |
| `run`         | function | Thread-pool parallel map with tqdm progress bar      |

## Signature

```python
run(
    func: Callable,
    args_list: List[tuple],
    n_jobs: int = -1,           # -1 → all CPU cores
    desc: str = "Processing",   # tqdm description
) -> List[Any]
```

Each entry of `args_list` is unpacked as `func(*entry)`. Return order
matches input order.

## Behavior

- Backed by `concurrent.futures.ThreadPoolExecutor` — threads, not
  processes.
- Progress bar via `tqdm` shows incremental completion.
- `n_jobs=-1` resolves to `os.cpu_count()`.
- Exceptions in `func` propagate after the pool drains.

## When to use

- I/O-bound: HTTP requests, file downloads, disk reads, S3 fan-out.
- Mixed CPU+I/O where the I/O dominates wall time.

## When NOT to use

- Pure CPU work — switch to `multiprocessing.Pool`, `joblib.Parallel`,
  or `dask`.
- Cross-machine fan-out — use `dask.distributed` or `ray`.

## Not exposed

- No process pool, no async/await variant, no result-streaming
  iterator. By design this module exposes one function and a version string.
