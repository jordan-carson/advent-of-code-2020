"""Pipeline stages built on queue.Queue, standing in for Go's unbuffered
channel. Python's stdlib has no true zero-capacity/rendezvous channel --
queue.Queue(maxsize=1), used elsewhere in this folder, is the closest
analog and is slightly more buffered than Go's real unbuffered channel (a
put() can succeed before anyone is waiting to get() it). This exercise
doesn't need that distinction: it's about the close-on-drain pipeline
*contract*, which is identical either way.

Python queues have no built-in close(). The convention here: a "closed"
queue ends with the module-level SENTINEL value instead of an exception.
"""
from __future__ import annotations

import queue
from typing import Any

SENTINEL = object()


def double(in_q: "queue.Queue[Any]") -> "queue.Queue[Any]":
    """Reads values from in_q until SENTINEL, doubling each one and
    putting it on the returned queue. Must put SENTINEL on the output
    once in_q is drained, so callers can pull until they see SENTINEL
    too. Do the reading in a background (daemon) thread so double()
    itself returns immediately -- this is a pipeline *stage*, not a
    blocking call. Stages built this way should compose:
    double(double(in_q)) must just work.
    """
    raise NotImplementedError
