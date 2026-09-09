"""Run with: python3 test_waitgroup.py"""
from __future__ import annotations

import threading

from waitgroup import WaitGroup, run_concurrently


def test_wait_group_basic() -> None:
    wg = WaitGroup()
    order = []
    lock = threading.Lock()

    def worker(n: int) -> None:
        with lock:
            order.append(n)
        wg.done()

    wg.add(3)
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
    for t in threads:
        t.start()
    wg.wait()
    for t in threads:
        t.join()
    assert sorted(order) == [0, 1, 2], f"order = {order}; want a permutation of [0, 1, 2]"


def test_wait_group_zero_immediately() -> None:
    wg = WaitGroup()
    wg.wait()  # must not block -- counter is already 0


def test_run_concurrently() -> None:
    tasks = [lambda: 10, lambda: 20, lambda: 30]
    got = run_concurrently(tasks)
    assert got == [10, 20, 30], f"run_concurrently(...) = {got}; want [10, 20, 30]"


def test_run_concurrently_at_scale() -> None:
    n = 500
    tasks = [(lambda i=i: i * i) for i in range(n)]
    want = [i * i for i in range(n)]
    got = run_concurrently(tasks)
    assert got == want, (
        "run_concurrently at scale did not preserve order or lost results -- "
        "check that add() is called before starting each thread, not inside it"
    )


def test_run_concurrently_empty() -> None:
    got = run_concurrently([])
    assert got == [], f"run_concurrently([]) = {got}; want []"


if __name__ == "__main__":
    test_wait_group_basic()
    print("test_wait_group_basic OK")
    test_wait_group_zero_immediately()
    print("test_wait_group_zero_immediately OK")
    test_run_concurrently()
    print("test_run_concurrently OK")
    test_run_concurrently_at_scale()
    print("test_run_concurrently_at_scale OK")
    test_run_concurrently_empty()
    print("test_run_concurrently_empty OK")
