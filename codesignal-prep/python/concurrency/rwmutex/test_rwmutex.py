"""Run with: python3 test_rwmutex.py"""
from __future__ import annotations

import threading
import time

from rwmutex import Cache, ReadWriteLock


def test_read_write_lock_allows_concurrent_readers() -> None:
    """Deterministic, not statistical: a Barrier forces all 5 readers to
    be inside the critical section at the same instant, so a correct
    ReadWriteLock must let peak concurrency reach exactly 5. A
    lock that (bug) only lets one reader in at a time will hang here
    until the test's own timeout fires on the barrier.
    """
    lock = ReadWriteLock()
    concurrent = 0
    peak = 0
    guard = threading.Lock()
    barrier = threading.Barrier(5, timeout=2.0)

    def reader() -> None:
        nonlocal concurrent, peak
        lock.acquire_read()
        try:
            with guard:
                concurrent += 1
                peak = max(peak, concurrent)
            barrier.wait()  # force all 5 readers to overlap right here
            with guard:
                concurrent -= 1
        finally:
            lock.release_read()

    threads = [threading.Thread(target=reader) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=5)

    assert peak == 5, f"peak concurrent readers = {peak}; want 5 (readers must not exclude each other)"


def test_read_write_lock_excludes_writer_from_readers() -> None:
    lock = ReadWriteLock()
    state: dict = {}

    def writer() -> None:
        lock.acquire_write()
        time.sleep(0.1)
        lock.release_write()

    def reader_attempt() -> None:
        time.sleep(0.02)  # start after the writer has (almost certainly) acquired
        start = time.monotonic()
        lock.acquire_read()
        state["reader_wait"] = time.monotonic() - start
        lock.release_read()

    t_writer = threading.Thread(target=writer)
    t_reader = threading.Thread(target=reader_attempt)
    t_writer.start()
    t_reader.start()
    t_writer.join(timeout=2)
    t_reader.join(timeout=2)

    waited = state.get("reader_wait")
    assert waited is not None, "reader_attempt never finished"
    assert waited >= 0.05, (
        f"reader acquired the read lock after only {waited:.3f}s; "
        "it should have waited for the writer to finish and release"
    )


def test_cache_get_set_basic() -> None:
    c = Cache()
    assert c.get("x") is None
    c.set("x", "hello")
    assert c.get("x") == "hello"


def test_cache_concurrent_readers_and_writers() -> None:
    c = Cache()
    c.set("key", "initial")

    def writer(worker_id: int) -> None:
        for i in range(200):
            c.set("key", f"writer-{worker_id}-{i}")

    def reader() -> None:
        for _ in range(200):
            assert c.get("key") is not None

    threads = [threading.Thread(target=writer, args=(w,)) for w in range(4)]
    threads += [threading.Thread(target=reader) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert c.get("key") is not None


if __name__ == "__main__":
    test_read_write_lock_allows_concurrent_readers()
    print("test_read_write_lock_allows_concurrent_readers OK")
    test_read_write_lock_excludes_writer_from_readers()
    print("test_read_write_lock_excludes_writer_from_readers OK")
    test_cache_get_set_basic()
    print("test_cache_get_set_basic OK")
    test_cache_concurrent_readers_and_writers()
    print("test_cache_concurrent_readers_and_writers OK")
