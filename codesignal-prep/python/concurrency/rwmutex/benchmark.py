"""ReadWriteLock.Cache vs. mutex.SafeMap, in two regimes.

Run after both rwmutex.py and ../mutex/mutex.py are implemented:

    python3 benchmark.py

Not part of the graded exercise -- this is the concrete "does RWMutex
actually help in Python?" demonstration the module docstring points you
at. Standard library only (concurrent.futures.ThreadPoolExecutor).

Two regimes, on purpose:

  1. Pure in-memory reads (a dict lookup, no I/O). Under CPython's GIL
     only one thread runs Python bytecode at a time regardless of which
     lock guards it, so there's no real parallelism for a plain Mutex to
     lose out on -- and ReadWriteLock's Condition-based bookkeeping costs
     more per call than Mutex's single acquire/release. Expect the plain
     Mutex to win or tie here. This is the opposite of the Go version's
     result, and that's the point: Go's RWMutex win comes from true OS
     -thread parallelism, which CPython threads don't have for pure
     Python code.

  2. Simulated I/O: the "read" itself is slow (e.g. a network or disk
     call) and held while the lock is on, using time.sleep() -- which
     does release the GIL. Now multiple readers can genuinely overlap,
     and ReadWriteLock should win by a wide margin.
"""
from __future__ import annotations

import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "mutex"))

from mutex import SafeMap  # noqa: E402
from rwmutex import Cache  # noqa: E402

WORKERS = 8


def _bench(fn, iterations: int) -> float:
    def hammer(_: int) -> None:
        for _ in range(iterations):
            fn()

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        list(pool.map(hammer, range(WORKERS)))
    return time.perf_counter() - start


def bench_in_memory() -> None:
    iterations = 50_000
    c = Cache()
    c.set("key", "value")
    m = SafeMap()
    m.increment("key", 1)

    rw_elapsed = _bench(lambda: c.get("key"), iterations)
    mx_elapsed = _bench(lambda: m.get("key"), iterations)

    print(f"[1] pure in-memory reads ({iterations * WORKERS} total, {WORKERS} threads):")
    print(f"    rwmutex.Cache : {rw_elapsed:.3f}s")
    print(f"    mutex.SafeMap : {mx_elapsed:.3f}s")
    winner = "mutex.SafeMap" if mx_elapsed < rw_elapsed else "rwmutex.Cache"
    print(f"    -> {winner} faster here (expected: mutex, under the GIL)")


def bench_simulated_io() -> None:
    iterations = 50
    delay = 0.002  # seconds the lock is held while "reading"

    rw_lock = Cache()._lock  # reuse the ReadWriteLock the Cache already built

    def rw_read() -> None:
        rw_lock.acquire_read()
        try:
            time.sleep(delay)
        finally:
            rw_lock.release_read()

    import threading

    mx_lock = threading.Lock()

    def mx_read() -> None:
        with mx_lock:
            time.sleep(delay)

    rw_elapsed = _bench(rw_read, iterations)
    mx_elapsed = _bench(mx_read, iterations)

    print(f"\n[2] simulated I/O ({delay * 1000:.0f}ms/op held under the lock, "
          f"{iterations * WORKERS} total, {WORKERS} threads):")
    print(f"    RWLock (readers overlap)   : {rw_elapsed:.3f}s")
    print(f"    plain Lock (serialized)    : {mx_elapsed:.3f}s")
    if rw_elapsed > 0:
        print(f"    -> RWLock {mx_elapsed / rw_elapsed:.1f}x faster here "
              f"(expected: a wide RWLock win, since sleep() releases the GIL)")


if __name__ == "__main__":
    bench_in_memory()
    bench_simulated_io()
