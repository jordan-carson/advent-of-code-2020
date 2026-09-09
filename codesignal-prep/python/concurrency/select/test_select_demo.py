"""Run with: python3 test_select_demo.py"""
from __future__ import annotations

import queue
import threading
import time

from select_demo import fan_in, select_receive

SENTINEL = object()


def test_fan_in() -> None:
    a: "queue.Queue" = queue.Queue()
    b: "queue.Queue" = queue.Queue()
    c: "queue.Queue" = queue.Queue()

    def feed(q: "queue.Queue", values) -> None:
        for v in values:
            q.put(v)
        q.put(SENTINEL)

    threading.Thread(target=feed, args=(a, [1, 2]), daemon=True).start()
    threading.Thread(target=feed, args=(b, [3]), daemon=True).start()
    threading.Thread(target=feed, args=(c, [4, 5]), daemon=True).start()

    out = fan_in(a, b, c, sentinel=SENTINEL)
    seen = set()
    while len(seen) < 5:
        try:
            v = out.get(timeout=2)
        except queue.Empty:
            raise AssertionError(f"timed out waiting for all 5 values, only saw {seen}")
        assert v is not SENTINEL, f"output closed early, only saw {seen}"
        seen.add(v)
    assert seen == {1, 2, 3, 4, 5}, f"fan_in output {seen}; want {{1, 2, 3, 4, 5}}"

    try:
        closer = out.get(timeout=1)
    except queue.Empty:
        raise AssertionError("output queue was never closed after all inputs finished")
    assert closer is SENTINEL, f"expected SENTINEL after all values, got {closer}"


def test_select_receive_success() -> None:
    q1: "queue.Queue" = queue.Queue()
    q2: "queue.Queue" = queue.Queue()
    q2.put(7)
    result = select_receive([q1, q2], timeout=0.5)
    assert result == (1, 7), f"select_receive(...) = {result}; want (1, 7)"


def test_select_receive_expires() -> None:
    q1: "queue.Queue" = queue.Queue()  # never sent to
    start = time.monotonic()
    result = select_receive([q1], timeout=0.1)
    elapsed = time.monotonic() - start
    assert result is None, f"select_receive(...) = {result}; want None"
    assert elapsed < 0.5, f"select_receive took {elapsed:.2f}s; should return promptly after its own timeout"


if __name__ == "__main__":
    test_fan_in()
    print("test_fan_in OK")
    test_select_receive_success()
    print("test_select_receive_success OK")
    test_select_receive_expires()
    print("test_select_receive_expires OK")
