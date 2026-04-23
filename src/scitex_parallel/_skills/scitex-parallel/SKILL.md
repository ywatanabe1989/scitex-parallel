---
name: scitex-parallel
description: Minimal thread-pool parallel execution for scientific Python — a single one-shot helper that maps a callable across argument tuples with auto CPU detection and a tqdm progress bar. Public API (1 symbol) — `run(func, args_list, n_jobs=-1, desc="Processing") -> List[Any]` (uses `ThreadPoolExecutor`, `n_jobs=-1` → `os.cpu_count()`, preserves input order in the result list, shows a `tqdm` bar labeled by `desc`). Thread-based, so best for I/O-bound workloads (HTTP fetches, file reads, API calls); CPU-bound loops remain GIL-limited — use `multiprocessing` / `joblib` / Dask / Ray for those. No CLI, no MCP tools, no extra modules. Drop-in replacement for `concurrent.futures.ThreadPoolExecutor(...).map(...)` with a manual `tqdm` wrapper, `joblib.Parallel(n_jobs=...)(delayed(f)(*a) for a in args)` (heavier dep, process-based default), and hand-rolled `threading.Thread` loops with `Queue`. Use whenever the user asks to "parallelize this loop with a progress bar", "download N URLs/PDFs in parallel", "fan out API calls across threads", "run a function over a list of arg tuples in parallel", or mentions `scitex.parallel.run`, thread pool with tqdm.
user-invocable: false
primary_interface: python
interfaces:
  python: 3
  cli: 0
  mcp: 0
  skills: 1
  hook: 0
  http: 0
---

# scitex-parallel

> **Interfaces:** Python ⭐⭐⭐ (primary) · CLI — · MCP — · Skills ⭐ · Hook — · HTTP —

One-function package: `run()` maps a callable over a list of argument
tuples using `ThreadPoolExecutor`. Use when you want a drop-in parallel
`map` with a progress bar and don't need `multiprocessing`, Dask, or Ray.

## Installation & import (two equivalent paths)

The same module is reachable via two install paths. Both forms work at
runtime; which one a user has depends on their install choice.

```python
# Standalone — pip install scitex-parallel
import scitex_parallel
scitex_parallel.run(...)

# Umbrella — pip install scitex
import scitex.parallel
scitex.parallel.run(...)
```

`pip install scitex-parallel` alone does NOT expose the `scitex` namespace;
`import scitex.parallel` raises `ModuleNotFoundError`. To use the
`scitex.parallel` form, also `pip install scitex`.

See [../../general/02_interface-python-api.md] for the ecosystem-wide
rule and empirical verification table.

Because it's thread-based, it's best for I/O-bound work; CPU-bound
workloads will be GIL-limited.

## Sub-skills

- [01_quick-start.md](01_quick-start.md) — install, import, one full example

No CLI, no MCP tools, no extra modules.
