"""Python's stdlib has no reader-writer lock (unlike Go's sync.RWMutex) --
you build one yourself from a Lock/Condition and a reader count. That's
this exercise's real content; Cache below is just something to guard
with it, same shape as the Go version.

Once ReadWriteLock passes, run benchmark.py. The result is NOT what the
Go version showed, and that gap is the actual lesson: under CPython's
GIL, only one thread runs Python bytecode at a time no matter which lock
you use, so a plain Mutex protecting a fast, pure-Python dict lookup
usually *beats* this RWLock -- the reader/writer bookkeeping costs more
than the (nonexistent) parallelism buys back. RWLock only pays off once
the protected work itself releases the GIL while it runs (real I/O, or a
C extension that drops the GIL) -- benchmark.py measures both cases so
you see the flip directly instead of taking it on faith.
"""
from __future__ import annotations

import threading
from typing import Dict, Optional


class ReadWriteLock:
    """Many readers may hold the lock at once; a writer excludes
    everyone -- other writers and all readers.
    """

    def __init__(self) -> None:
        self._condition = threading.Condition()
        self._readers = 0
        self._writer_active = False

    def acquire_read(self) -> None:
        raise NotImplementedError

    def release_read(self) -> None:
        raise NotImplementedError

    def acquire_write(self) -> None:
        raise NotImplementedError

    def release_write(self) -> None:
        raise NotImplementedError


class Cache:
    def __init__(self) -> None:
        self._lock = ReadWriteLock()
        self._data: Dict[str, str] = {}

    def get(self, key: str) -> Optional[str]:
        """Must use acquire_read/release_read -- that's the entire point of this type."""
        raise NotImplementedError

    def set(self, key: str, value: str) -> None:
        raise NotImplementedError
