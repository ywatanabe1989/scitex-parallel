---
description: |
  [TOPIC] scitex-parallel Quick Start
  [DETAILS] Smallest example — map a function over arg tuples on a thread pool with tqdm.
tags: [scitex-parallel-quick-start]
---

# Quick Start

## Run a function over many argument tuples

```python
from scitex_parallel import run

def add(x, y):
    return x + y

args_list = [(1, 4), (2, 5), (3, 6)]
results = run(add, args_list, n_jobs=-1, desc="adding")
# results == [5, 7, 9]   (order preserved)
```

Each entry of `args_list` is unpacked as `func(*entry)`.

## Real example — parallel HTTP

```python
import requests
from scitex_parallel import run

def fetch(url):
    return requests.get(url).status_code

urls = [("https://example.com",), ("https://www.python.org",)]
codes = run(fetch, urls, n_jobs=8, desc="fetching")
```

Best fit: I/O-bound work where the GIL is not the bottleneck.

## Keyword-only callables

`run` only forwards positional args. Wrap in a small adapter:

```python
def _adapter(args):
    a, kwargs = args
    return real_func(*a, **kwargs)

run(_adapter, [((1,), {"key": "v"})], n_jobs=4)
```
