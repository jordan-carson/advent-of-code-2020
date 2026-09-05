"""Implement RateLimiter level by level. See README.md for the spec."""
from __future__ import annotations


class RateLimiter:
    def __init__(self, limit: int, window_seconds: float) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        # TODO: design your Level 1 per-client state here

    # --- Level 1 ---
    def allow(self, client_id: str, now: float) -> bool:
        raise NotImplementedError

    # --- Level 2 ---
    def allow_sliding(self, client_id: str, now: float) -> bool:
        raise NotImplementedError

    # --- Level 3 ---
    def set_limit(self, client_id: str, limit: int, window_seconds: float) -> None:
        raise NotImplementedError

    # --- Level 4 ---
    def allow_bucket(self, client_id: str, now: float, cost: int = 1) -> bool:
        raise NotImplementedError


def test_level_1() -> None:
    limiter = RateLimiter(limit=2, window_seconds=10)
    assert limiter.allow("c1", now=0) is True
    assert limiter.allow("c1", now=1) is True
    assert limiter.allow("c1", now=2) is False  # limit exhausted in this window
    assert limiter.allow("c1", now=11) is True  # new window


def test_level_2() -> None:
    limiter = RateLimiter(limit=2, window_seconds=10)
    assert limiter.allow_sliding("c1", now=0) is True
    assert limiter.allow_sliding("c1", now=5) is True
    assert limiter.allow_sliding("c1", now=6) is False
    assert limiter.allow_sliding("c1", now=11) is True  # the t=0 request has aged out


def test_level_3() -> None:
    limiter = RateLimiter(limit=1, window_seconds=10)
    limiter.set_limit("vip", limit=5, window_seconds=10)
    for i in range(5):
        assert limiter.allow("vip", now=i) is True
    assert limiter.allow("vip", now=5) is False
    assert limiter.allow("regular", now=0) is True
    assert limiter.allow("regular", now=1) is False


if __name__ == "__main__":
    test_level_1()
    print("Level 1 OK")
    test_level_2()
    print("Level 2 OK")
    test_level_3()
    print("Level 3 OK")
