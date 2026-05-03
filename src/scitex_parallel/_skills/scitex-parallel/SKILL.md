---
name: scitex-parallel
description: |
  [WHAT] Minimal thread-pool parallel execution for scientific Python — a single one-shot helper that maps a callable across argument tuples with auto CPU detection and a tqdm progress bar.
  [WHEN] Use whenever the user asks to "parallelize this loop with a progress bar", "download N URLs/PDFs in parallel", "fan out API calls across threads", "run a function over a list of arg tuples in parallel", or mentions `scitex.
  [HOW] `pip install scitex-parallel` then `import scitex_parallel`; see leaf skills for details.
tags: [scitex-parallel]
primary_interface: python
interfaces:
  python: 3
  cli: 0
  mcp: 0
  skills: 1
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
