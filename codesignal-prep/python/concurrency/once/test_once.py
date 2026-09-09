"""Run with: python3 test_once.py"""
from __future__ import annotations

import threading
import time

from once import Loader


def test_get_calls_load_exactly_once() -> None:
    loader = Loader()
    calls = []
    calls_lock = threading.Lock()
    n = 100
    results = [None] * n

    def worker(idx: int) -> None:
        def load() -> str:
            with calls_lock:
                calls.append(1)
            time.sleep(0.01)  # widen the race window
            return "loaded-value"

        results[idx] = loader.get(load)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(calls) == 1, f"load was called {len(calls)} times across {n} concurrent get() calls; want exactly 1"
    assert all(r == "loaded-value" for r in results), f"not all callers got the loaded value: {results}"


def test_get_ignores_load_on_subsequent_calls() -> None:
    loader = Loader()
    first = loader.get(lambda: "first")
    second = loader.get(lambda: "second")
    assert first == "first" and second == "first", (
        f"got {first!r} then {second!r}; want 'first' then 'first' (second load must never run)"
    )


if __name__ == "__main__":
    test_get_calls_load_exactly_once()
    print("test_get_calls_load_exactly_once OK")
    test_get_ignores_load_on_subsequent_calls()
    print("test_get_ignores_load_on_subsequent_calls OK")
