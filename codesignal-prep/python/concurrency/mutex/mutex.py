"""threading.Lock is Python's sync.Mutex -- non-reentrant, same contract.
This exercise makes a shared dict safe for concurrent use.

Python's GIL does NOT make `self._data[key] = self._data.get(key, 0) +
delta` safe across threads on its own: that's several separate bytecode
operations (a get, an add, a set), and the interpreter can switch
threads between any of them. Run test_mutex.py's stress test to see it
matter.
"""
from __future__ import annotations

import threading
from typing import Dict, Optional


class SafeMap:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._data: Dict[str, int] = {}

    def get(self, key: str) -> Optional[int]:
        raise NotImplementedError

    def increment(self, key: str, delta: int) -> int:
        """Adds delta to key's current value (0 if unset) and returns the
        new value. Must be atomic end-to-end -- a read-then-write built
        from two separately-locked calls to get()/a plain assignment
        would lose updates under concurrent callers incrementing the
        same key.
        """
        raise NotImplementedError
