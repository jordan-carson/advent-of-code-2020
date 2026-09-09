"""Run with: python3 test_ownership.py"""
from __future__ import annotations

import sys
import threading

from ownership import OwnedCounter, SharedCounter

# Force much more frequent thread switches than CPython's 5ms default --
# without this, a read-modify-write race on SharedCounter rarely lands in
# the danger window often enough in a short run to actually catch it.
sys.setswitchinterval(1e-6)

WORKERS = 60
PER_WORKER = 500
TOTAL = WORKERS * PER_WORKER


def test_shared_counter_concurrent() -> None:
    counter = SharedCounter()

    def worker() -> None:
        for _ in range(PER_WORKER):
            counter.increment()

    threads = [threading.Thread(target=worker) for _ in range(WORKERS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    got = counter.value()
    assert got == TOTAL, f"value() = {got}; want {TOTAL} (lost updates -- is increment() actually locking?)"


def test_owned_counter_concurrent() -> None:
    counter = OwnedCounter()

    def worker() -> None:
        for _ in range(PER_WORKER):
            counter.increment()

    threads = [threading.Thread(target=worker) for _ in range(WORKERS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    got = counter.value()
    assert got == TOTAL, f"value() = {got}; want {TOTAL}"


if __name__ == "__main__":
    test_shared_counter_concurrent()
    print("test_shared_counter_concurrent OK")
    test_owned_counter_concurrent()
    print("test_owned_counter_concurrent OK")
