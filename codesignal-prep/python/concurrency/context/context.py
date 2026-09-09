"""Python's stdlib has nothing like context.Context for plain threads
(asyncio has its own different, cooperative-cancellation story that
doesn't apply to OS threads and isn't what's being drilled here). Build a
minimal one: a cancellation flag plus an optional deadline, and the two
patterns context.Context is actually used for -- racing real work against
cancellation, and a loop that checks for cancellation instead of running
forever.
"""
from __future__ import annotations

import threading
import time
from typing import Callable, Optional, Tuple


class CancelledError(Exception):
    pass


class CancelContext:
    def __init__(self, timeout: Optional[float] = None) -> None:
        """timeout is seconds from creation, or None for no deadline."""
        self._event = threading.Event()
        self._deadline = (time.monotonic() + timeout) if timeout is not None else None

    def cancel(self) -> None:
        raise NotImplementedError

    def is_cancelled(self) -> bool:
        """True once cancel() has been called, or the deadline (if any)
        has passed.
        """
        raise NotImplementedError

    def wait(self, timeout: Optional[float] = None) -> bool:
        """Blocks until cancelled, the deadline passes, or `timeout`
        elapses -- whichever comes first. Returns True if cancelled or
        the deadline passed, False if `timeout` elapsed with neither.
        """
        raise NotImplementedError


def run_with_timeout(
    ctx: CancelContext, work: Callable[[], int]
) -> Tuple[Optional[int], Optional[Exception]]:
    """Runs work in its own thread and returns (result, None), unless
    ctx is cancelled or times out first -- in which case it returns
    (None, CancelledError(...)) immediately, without waiting for work to
    finish.
    """
    raise NotImplementedError


def count_until_cancel(ctx: CancelContext, tick: float) -> int:
    """Increments a counter once per tick until ctx is cancelled, then
    returns the final count. Must notice cancellation promptly (within
    about one tick), not run to some fixed limit.
    """
    raise NotImplementedError
