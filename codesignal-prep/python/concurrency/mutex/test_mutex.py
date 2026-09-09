"""Run with: python3 test_mutex.py

Python has no `-race` flag -- there's no built-in dynamic race detector
the way Go has. These tests can only catch bugs statistically, by
hammering shared state hard enough that an unsynchronized implementation
is very likely (not guaranteed) to lose an update. If test_mutex.py
passes, that's meaningful evidence, not a proof of race-freedom.
"""
from __future__ import annotations

import sys
import threading

from mutex import SafeMap

# Force much more frequent thread switches than CPython's 5ms default.
# Without this, a read-modify-write race rarely lands in the danger
# window often enough in a run this short to actually flip the test --
# the switch interval, not the iteration count, is what makes this test
# reliable rather than lucky.
sys.setswitchinterval(1e-6)


def test_get_set_basic() -> None:
    m = SafeMap()
    assert m.get("x") is None, "Get on missing key should be None"
    got = m.increment("x", 5)
    assert got == 5, f"increment(x, 5) = {got}; want 5"
    assert m.get("x") == 5, f"get(x) = {m.get('x')}; want 5"


def test_increment_is_atomic_under_concurrency() -> None:
    m = SafeMap()
    goroutines = 50
    per_goroutine = 400

    def worker() -> None:
        for _ in range(per_goroutine):
            m.increment("shared", 1)

    threads = [threading.Thread(target=worker) for _ in range(goroutines)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    want = goroutines * per_goroutine
    got = m.get("shared")
    assert got == want, f"get(shared) = {got}; want {want} (lost updates under concurrency)"


if __name__ == "__main__":
    test_get_set_basic()
    print("test_get_set_basic OK")
    test_increment_is_atomic_under_concurrency()
    print("test_increment_is_atomic_under_concurrency OK")
