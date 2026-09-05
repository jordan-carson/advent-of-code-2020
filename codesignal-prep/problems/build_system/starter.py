"""Implement BuildSystem level by level. See README.md for the spec."""
from __future__ import annotations

from typing import Callable


class BuildSystem:
    def __init__(self) -> None:
        pass  # TODO: design your Level 1 state here

    # --- Level 1 ---
    def add_task(self, name: str, dependencies: list[str] | None = None) -> None:
        raise NotImplementedError

    def build_order(self, target: str) -> list[str] | None:
        raise NotImplementedError

    # --- Level 2 ---
    def run(self, target: str, executor: Callable[[str], None]) -> list[str]:
        raise NotImplementedError

    # --- Level 3 ---
    def mark_dirty(self, name: str) -> None:
        raise NotImplementedError


def test_level_1() -> None:
    bs = BuildSystem()
    bs.add_task("compile", ["fetch_deps"])
    bs.add_task("fetch_deps", [])
    bs.add_task("test", ["compile"])
    order = bs.build_order("test")
    assert order is not None
    assert order.index("fetch_deps") < order.index("compile") < order.index("test")

    bs2 = BuildSystem()
    bs2.add_task("a", ["b"])
    bs2.add_task("b", ["a"])
    assert bs2.build_order("a") is None


def test_level_2() -> None:
    bs = BuildSystem()
    bs.add_task("compile", ["fetch_deps"])
    bs.add_task("fetch_deps", [])
    executed = []
    order = bs.run("compile", executor=executed.append)
    assert executed == order == ["fetch_deps", "compile"]


def test_level_3() -> None:
    bs = BuildSystem()
    bs.add_task("compile", ["fetch_deps"])
    bs.add_task("fetch_deps", [])
    bs.add_task("test", ["compile"])
    executed = []
    bs.run("test", executor=executed.append)
    assert executed == ["fetch_deps", "compile", "test"]

    executed.clear()
    bs.run("test", executor=executed.append)
    assert executed == []  # nothing dirty, nothing to do

    bs.mark_dirty("fetch_deps")
    executed.clear()
    bs.run("test", executor=executed.append)
    assert executed == ["fetch_deps", "compile", "test"]  # whole downstream chain


if __name__ == "__main__":
    test_level_1()
    print("Level 1 OK")
    test_level_2()
    print("Level 2 OK")
    test_level_3()
    print("Level 3 OK")
