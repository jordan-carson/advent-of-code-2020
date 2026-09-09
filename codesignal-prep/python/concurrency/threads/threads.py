"""The warm-up (Python's analog of Go's goroutines/ drill): spawn one
thread per unit of work, and know when they're all done -- without any
synchronization primitive beyond a plain list of threads to join().

A Python `threading.Thread` is a real OS thread, not a lightweight
green goroutine -- creating thousands of them is a lot heavier than Go
would tolerate -- but the fan-out/fan-in shape you're drilling here is
identical, and it's the shape every other exercise in this folder builds
on.
"""
from __future__ import annotations

from typing import List


def squares(nums: List[int]) -> List[int]:
    """Compute the square of each number concurrently -- one thread per
    element -- and return results in the same order as the input. Each
    thread should write only to its own index of the result list
    (distinct indices are safe to write concurrently, no lock needed);
    the function must not return until every thread has finished.
    """
    raise NotImplementedError
