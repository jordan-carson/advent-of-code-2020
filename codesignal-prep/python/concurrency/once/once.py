"""Python's stdlib has no sync.Once either -- build the classic "exactly
once, even under a race to be first" pattern from a Lock plus a flag
(double-checked locking).

Real Python code often sidesteps this by doing expensive setup at module
import time, since CPython's import system already guarantees that runs
exactly once (GIL-protected) -- but that only covers import-time
constants, not "the first time this runtime value is actually needed,"
which is what Once is for.
"""
from __future__ import annotations

import threading
from typing import Callable, Optional


class Once:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._done = False

    def do(self, fn: Callable[[], None]) -> None:
        """Calls fn the first time do() is ever invoked on this Once,
        across however many threads call it concurrently -- and never
        again after that, even if a *different* fn is passed on a later
        call.
        """
        raise NotImplementedError


class Loader:
    def __init__(self) -> None:
        self._once = Once()
        self._value: Optional[str] = None

    def get(self, load: Callable[[], str]) -> str:
        """Returns the loaded value, calling load exactly once across
        all concurrent callers -- even if many threads call get() before
        the first load finishes, they must all block until that one load
        completes and then all receive its result.
        """
        raise NotImplementedError
