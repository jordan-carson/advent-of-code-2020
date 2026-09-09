"""Run with: python3 test_threads.py"""
from __future__ import annotations

from threads import squares


def test_squares() -> None:
    got = squares([1, 2, 3, 4, 5])
    want = [1, 4, 9, 16, 25]
    assert got == want, f"squares(...) = {got}; want {want}"


def test_squares_preserves_order_at_scale() -> None:
    nums = list(range(500))
    want = [n * n for n in nums]
    got = squares(nums)
    assert got == want, "squares at scale did not preserve input order"


def test_squares_empty() -> None:
    got = squares([])
    assert got == [], f"squares([]) = {got}; want []"


if __name__ == "__main__":
    test_squares()
    print("test_squares OK")
    test_squares_preserves_order_at_scale()
    print("test_squares_preserves_order_at_scale OK")
    test_squares_empty()
    print("test_squares_empty OK")
