"""Run with: python3 test_channels.py"""
from __future__ import annotations

import queue

from channels import SENTINEL, double


def _drain(q: "queue.Queue", timeout: float = 2.0) -> list:
    out = []
    while True:
        try:
            v = q.get(timeout=timeout)
        except queue.Empty:
            raise AssertionError(
                "timed out waiting for SENTINEL -- did double() put it once in_q was drained?"
            )
        if v is SENTINEL:
            return out
        out.append(v)


def test_double() -> None:
    in_q: "queue.Queue" = queue.Queue()
    for n in (1, 2, 3):
        in_q.put(n)
    in_q.put(SENTINEL)
    got = _drain(double(in_q))
    assert got == [2, 4, 6], f"double(...) drained to {got}; want [2, 4, 6]"


def test_double_chaining() -> None:
    in_q: "queue.Queue" = queue.Queue()
    in_q.put(1)
    in_q.put(2)
    in_q.put(SENTINEL)
    got = _drain(double(double(in_q)))
    assert got == [4, 8], f"chained double(double(...)) drained to {got}; want [4, 8]"


def test_double_empty_input() -> None:
    in_q: "queue.Queue" = queue.Queue()
    in_q.put(SENTINEL)
    got = _drain(double(in_q))
    assert got == [], f"double(empty) drained to {got}; want []"


if __name__ == "__main__":
    test_double()
    print("test_double OK")
    test_double_chaining()
    print("test_double_chaining OK")
    test_double_empty_input()
    print("test_double_empty_input OK")
