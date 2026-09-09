"""Ownership vs. shared memory -- the Python translation of Go's
"don't communicate by sharing memory; share memory by communicating."

Implement the same counter twice:
  - SharedCounter: a threading.Lock guards state any thread can touch.
  - OwnedCounter: a single dedicated thread owns the state; every other
    thread talks to it by putting messages on a queue.Queue. No
    attribute is ever read or written from more than one thread, so
    there's nothing to lock.

Python's GIL does NOT make a read-modify-write of shared state safe
across threads on its own -- it's several separate bytecode instructions,
and the interpreter can switch threads between any of them. Storage below
is deliberately a dict with a `.get()` read rather than a plain instance
attribute: CPython 3.11+'s specializing interpreter turns a bare
`self._value += 1` into bytecode tight enough that the race almost never
shows up in a stress test in practice, even though it's still just as
unsafe -- the dict/.get() shape here is what actually keeps the exercise
honest. Fill both in and prove it with test_ownership.py.
"""
from __future__ import annotations

import queue
import threading
from typing import Dict, Optional


class SharedCounter:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._data: Dict[str, int] = {}

    def increment(self, delta: int = 1) -> None:
        raise NotImplementedError

    def value(self) -> int:
        raise NotImplementedError


class _Command:
    """A message sent to the owning thread. delta=0 with a reply queue
    means "don't change anything, just send me the current value."
    """

    __slots__ = ("delta", "reply")

    def __init__(self, delta: int, reply: "Optional[queue.Queue[int]]") -> None:
        self.delta = delta
        self.reply = reply


class OwnedCounter:
    def __init__(self) -> None:
        self._commands: "queue.Queue[_Command]" = queue.Queue()
        # TODO: start a daemon thread running self._run() -- it must be
        # the *only* code that ever reads or writes the counter's value.

    def _run(self) -> None:
        raise NotImplementedError

    def increment(self, delta: int = 1) -> None:
        raise NotImplementedError

    def value(self) -> int:
        raise NotImplementedError
