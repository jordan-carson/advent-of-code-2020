"""Implement KeyValueStore level by level. See README.md for the spec.

No solution code here on purpose -- fill in the TODOs yourself, without AI
assistance, under a timer (see ../../timer.py). Each `test_level_N` function
is a plain-assert smoke test you should extend with your own edge cases
before moving to the next level.
"""
from __future__ import annotations


class KeyValueStore:
    def __init__(self) -> None:
        pass  # TODO: design your Level 1 state here

    # --- Level 1 ---
    def set(self, key: str, value: str) -> None:
        raise NotImplementedError

    def get(self, key: str) -> str | None:
        raise NotImplementedError

    def delete(self, key: str) -> bool:
        raise NotImplementedError

    # --- Level 2 ---
    def scan(self, prefix: str) -> list[str]:
        raise NotImplementedError

    def scan_range(self, start: str, end: str) -> list[str]:
        raise NotImplementedError

    # --- Level 3 ---
    def set_with_ttl(self, key: str, value: str, ttl_seconds: float) -> None:
        raise NotImplementedError

    # --- Level 4 ---
    def snapshot(self) -> dict:
        raise NotImplementedError

    def restore(self, snapshot: dict) -> None:
        raise NotImplementedError

    # --- Level 5 (stretch) ---
    def begin(self) -> None:
        raise NotImplementedError

    def commit(self) -> None:
        raise NotImplementedError

    def rollback(self) -> None:
        raise NotImplementedError


def test_level_1() -> None:
    store = KeyValueStore()
    assert store.get("a") is None
    store.set("a", "1")
    assert store.get("a") == "1"
    store.set("a", "2")
    assert store.get("a") == "2"
    assert store.delete("a") is True
    assert store.delete("a") is False
    assert store.get("a") is None


def test_level_2() -> None:
    store = KeyValueStore()
    for key in ["apple", "app", "banana", "apricot"]:
        store.set(key, key.upper())
    assert store.scan("ap") == ["app", "apple", "apricot"]
    assert store.scan_range("apple", "banana") == ["apple", "apricot", "banana"]


def test_level_3() -> None:
    import time

    store = KeyValueStore()
    store.set_with_ttl("temp", "v", ttl_seconds=0.05)
    assert store.get("temp") == "v"
    time.sleep(0.1)
    assert store.get("temp") is None
    assert store.scan("t") == []


def test_level_4() -> None:
    store = KeyValueStore()
    store.set("a", "1")
    store.set("b", "2")
    snap = store.snapshot()
    store.set("a", "changed")
    store.delete("b")
    store.restore(snap)
    assert store.get("a") == "1"
    assert store.get("b") == "2"


if __name__ == "__main__":
    test_level_1()
    print("Level 1 OK")
    test_level_2()
    print("Level 2 OK")
    test_level_3()
    print("Level 3 OK")
    test_level_4()
    print("Level 4 OK")
