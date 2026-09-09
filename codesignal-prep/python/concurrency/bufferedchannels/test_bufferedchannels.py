"""Run with: python3 test_bufferedchannels.py"""
from __future__ import annotations

import threading

from bufferedchannels import BoundedQueue


def test_try_push_when_full() -> None:
    q = BoundedQueue(2)
    assert q.try_push(1) is True, "try_push should succeed while under capacity"
    assert q.try_push(2) is True, "try_push should succeed while under capacity"
    assert q.try_push(3) is False, "try_push should fail once the queue is at capacity"


def test_push_blocks_until_room() -> None:
    q = BoundedQueue(1)
    q.push(1)  # fill it to capacity

    done = threading.Event()

    def pusher() -> None:
        q.push(2)  # must block until pop() below makes room
        done.set()

    threading.Thread(target=pusher, daemon=True).start()

    assert not done.wait(timeout=0.1), "push on a full queue returned before room was made"

    got = q.pop()
    assert got == 1, f"pop() = {got}; want 1 (FIFO order)"

    assert done.wait(timeout=1.0), "push did not unblock after pop made room"
    got = q.pop()
    assert got == 2, f"pop() = {got}; want 2"


def test_pop_blocks_until_available() -> None:
    q = BoundedQueue(1)
    results = []
    done = threading.Event()

    def popper() -> None:
        results.append(q.pop())
        done.set()

    threading.Thread(target=popper, daemon=True).start()

    assert not done.wait(timeout=0.1), "pop on an empty queue returned before anything was pushed"

    q.push(42)

    assert done.wait(timeout=1.0), "pop did not unblock after push"
    assert results == [42], f"popper got {results}; want [42]"


if __name__ == "__main__":
    test_try_push_when_full()
    print("test_try_push_when_full OK")
    test_push_blocks_until_room()
    print("test_push_blocks_until_room OK")
    test_pop_blocks_until_available()
    print("test_pop_blocks_until_available OK")
