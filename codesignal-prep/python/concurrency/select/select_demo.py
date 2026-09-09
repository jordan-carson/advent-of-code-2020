"""Go's `select` does two jobs: merge multiple channels (fan-in), and
race a receive against a timeout. Python's queue.Queue has no built-in
"wait on any of these queues" operation -- unlike the Go runtime, which
has direct scheduler support for selecting over channels, the standard
Python workaround is polling: check each queue with get_nowait() in a
loop, sleeping briefly between passes. It's less elegant than Go's
select, and it's exactly what real Python code reaches for in this
situation, so it's worth building deliberately rather than only
stumbling into it. (Module named select_demo.py, not select.py, so it
doesn't shadow the stdlib `select` module.)

fan_in below is a different, more idiomatic shape: when you control the
producers, you don't need select_receive at all -- just have every
producer thread put directly onto one shared output queue. That's the
pattern real Python fan-in code uses; select_receive is for when you're
handed multiple existing queues you don't control.
"""
from __future__ import annotations

import queue
from typing import Optional, Sequence, Tuple


def select_receive(
    queues: Sequence["queue.Queue"], timeout: float, poll_interval: float = 0.005
) -> Optional[Tuple[int, object]]:
    """Waits for a value on any of `queues`. Returns (index, value) for
    whichever queue produced something first, or None if nothing arrives
    within timeout. Must not busy-loop hot -- sleep poll_interval between
    polling passes.
    """
    raise NotImplementedError


def fan_in(*queues: "queue.Queue", sentinel: object) -> "queue.Queue":
    """Merges values from multiple input queues into a single output
    queue, in whatever order they actually arrive. Each input queue ends
    with `sentinel`; put `sentinel` on the output once every input has
    delivered its own sentinel.
    """
    raise NotImplementedError
