"""Python's idiomatic answer to "wait for N threads to finish" is just
keeping a list of Thread objects and calling .join() on each -- there's
no stdlib WaitGroup. Building one yourself here is the point: it's the
same reference-counting-plus-condition-variable pattern behind a lot of
real synchronization primitives, and it mirrors Go's sync.WaitGroup
closely enough to carry over directly.

Classic footgun (same one Go's sync.WaitGroup has): call add() before
starting the thread, never from inside the thread -- if the thread
hasn't been scheduled yet, a concurrent wait() can return before add()
ever ran.
"""
from __future__ import annotations

import threading
from typing import Callable, List


class WaitGroup:
    def __init__(self) -> None:
        self._condition = threading.Condition()
        self._count = 0

    def add(self, delta: int = 1) -> None:
        raise NotImplementedError

    def done(self) -> None:
        """Equivalent to add(-1)."""
        raise NotImplementedError

    def wait(self) -> None:
        """Blocks until the counter returns to zero. Must return
        immediately if the counter is already zero.
        """
        raise NotImplementedError


def run_concurrently(tasks: List[Callable[[], int]]) -> List[int]:
    """Runs each task in its own thread and returns their results in the
    same order as tasks, using the WaitGroup above to know when every
    thread has finished.
    """
    raise NotImplementedError
