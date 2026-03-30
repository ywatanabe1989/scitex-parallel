#!/usr/bin/env python3
# File: src/scitex_parallel/_run.py

"""
Parallel execution utilities using ThreadPoolExecutor.

1. Functionality:
   - Runs functions in parallel using ThreadPoolExecutor
   - Handles both single and multiple return values
   - Supports automatic CPU core detection
2. Input:
   - Function to run
   - List of items to process
   - Optional parameters for execution control
3. Output:
   - List of results or concatenated tuple
4. Prerequisites:
   - concurrent.futures
   - tqdm
"""

import multiprocessing
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, List

from tqdm import tqdm


def run(
    func: Callable,
    args_list: List[tuple],
    n_jobs: int = -1,
    desc: str = "Processing",
) -> List[Any]:
    """Runs function in parallel using ThreadPoolExecutor with tuple arguments.

    Parameters
    ----------
    func : Callable
        Function to run in parallel
    args_list : List[tuple]
        List of argument tuples, each tuple contains arguments for one function call
    n_jobs : int, optional
        Number of jobs to run in parallel. -1 means using all processors
    desc : str, optional
        Description for progress bar

    Returns
    -------
    List[Any]
        Results of parallel execution

    Examples
    --------
    >>> def add(x, y):
    ...     return x + y
    >>> args_list = [(1, 4), (2, 5), (3, 6)]
    >>> run(add, args_list)
    [5, 7, 9]
    """
    if not args_list:
        raise ValueError("Args list cannot be empty")
    if not callable(func):
        raise ValueError("Func must be callable")

    # Validate n_jobs before conversion: must be -1 or >= 1
    if n_jobs < -1 or n_jobs == 0:
        raise ValueError("n_jobs must be >= 1 or -1")

    cpu_count = multiprocessing.cpu_count()
    n_jobs = cpu_count if n_jobs == -1 else n_jobs

    if n_jobs > cpu_count:
        warnings.warn(f"n_jobs ({n_jobs}) is greater than CPU count ({cpu_count})")

    results = [None] * len(args_list)  # Pre-allocate list

    with ThreadPoolExecutor(max_workers=n_jobs) as executor:
        futures = {
            executor.submit(func, *args): idx for idx, args in enumerate(args_list)
        }
        for future in tqdm(as_completed(futures), total=len(args_list), desc=desc):
            idx = futures[future]
            results[idx] = future.result()

    # If results contain multiple values (tuples), transpose them
    if results and isinstance(results[0], tuple):
        n_vars = len(results[0])
        return tuple([result[i] for result in results] for i in range(n_vars))

    return results


# EOF
