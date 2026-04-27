"""scitex-parallel quickstart: parallel run over a callable with tuple args."""

import time

import scitex_parallel


def add(x, y):
    return x + y


def main():
    # 1. Build args list — each tuple is one function call.
    args_list = [(i, i + 1) for i in range(8)]
    expected = [a + b for a, b in args_list]

    # 2. scitex_parallel.run — parallel execution returning a list of results.
    t0 = time.perf_counter()
    results = scitex_parallel.run(add, args_list, n_jobs=4, desc="parallel")
    elapsed = time.perf_counter() - t0
    print("results:", results)
    print(f"elapsed: {elapsed:.3f}s")
    assert results == expected

    # 3. n_jobs=1 acts as a serial fallback (deterministic order).
    serial = scitex_parallel.run(add, args_list, n_jobs=1, desc="serial")
    print("serial:", serial)
    assert serial == expected


if __name__ == "__main__":
    main()
