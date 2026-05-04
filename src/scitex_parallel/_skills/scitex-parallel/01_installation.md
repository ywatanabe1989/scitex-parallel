---
description: |
  [TOPIC] scitex-parallel Installation
  [DETAILS] pip install scitex-parallel; tqdm-backed; smoke verify with run().
tags: [scitex-parallel-installation]
---

# Installation

## Standard

```bash
pip install scitex-parallel
```

Pulls `tqdm` for the progress bar. `ThreadPoolExecutor` is from the
standard library.

## Umbrella

```bash
pip install scitex            # also exposes the same module as scitex.parallel
```

`pip install scitex-parallel` alone does NOT make `import scitex.parallel`
work — install the umbrella for that form. See
`../../general/02_interface-python-api.md`.

## Verify

```bash
python -c "from scitex_parallel import run; print(run(lambda x: x*2, [(i,) for i in range(5)]))"
```

Expected: `[0, 2, 4, 6, 8]` and a tqdm bar flashing past.

## When NOT to install

- CPU-bound numeric loops — threads are GIL-limited; reach for
  `multiprocessing`, `joblib`, or `dask` instead.
- Distributed work across machines — use `dask.distributed` or `ray`.

This package is a deliberately minimal one-function helper for I/O-bound
work (HTTP requests, file downloads, S3 fan-out).
