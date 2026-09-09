"""A Go buffered channel's behavior -- bounded capacity, Push blocks when
full, Pop blocks when empty -- is exactly what queue.Queue(maxsize=N)
already gives you for free. This exercise is about using it correctly,
including the non-blocking variant: Go's `select` with a `default` case
becomes Python's put_nowait()/get_nowait() plus catching queue.Full /
queue.Empty.
"""
from __future__ import annotations

import queue


class BoundedQueue:
    def __init__(self, capacity: int) -> None:
        self._items: "queue.Queue[int]" = queue.Queue(maxsize=capacity)

    def push(self, item: int) -> None:
        """Blocks until there is room in the queue."""
        raise NotImplementedError

    def try_push(self, item: int) -> bool:
        """Returns False immediately if the queue is at capacity, instead
        of blocking.
        """
        raise NotImplementedError

    def pop(self) -> int:
        """Blocks until an item is available."""
        raise NotImplementedError
