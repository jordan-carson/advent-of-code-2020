"""Implement PackageManager level by level. See README.md for the spec."""
from __future__ import annotations


class PackageManager:
    def __init__(self) -> None:
        pass  # TODO: design your Level 1 state here (think graph representation)

    # --- Level 1 ---
    def add_package(self, name: str, version: str, dependencies: list[str] | None = None) -> None:
        raise NotImplementedError

    def install(self, name: str) -> list[str] | None:
        raise NotImplementedError


def test_level_1_linear() -> None:
    pm = PackageManager()
    pm.add_package("base", "1.0", [])
    pm.add_package("mid", "1.0", ["base"])
    pm.add_package("top", "1.0", ["mid"])
    order = pm.install("top")
    assert order is not None
    assert order.index("base") < order.index("mid") < order.index("top")


def test_level_1_cycle() -> None:
    pm = PackageManager()
    pm.add_package("a", "1.0", ["b"])
    pm.add_package("b", "1.0", ["a"])
    assert pm.install("a") is None


def test_level_1_diamond() -> None:
    pm = PackageManager()
    pm.add_package("base", "1.0", [])
    pm.add_package("left", "1.0", ["base"])
    pm.add_package("right", "1.0", ["base"])
    pm.add_package("top", "1.0", ["left", "right"])
    order = pm.install("top")
    assert order is not None
    assert order.count("base") == 1
    assert order.index("base") < order.index("left")
    assert order.index("base") < order.index("right")
    assert order.index("left") < order.index("top")
    assert order.index("right") < order.index("top")


if __name__ == "__main__":
    test_level_1_linear()
    test_level_1_cycle()
    test_level_1_diamond()
    print("Level 1 OK")
