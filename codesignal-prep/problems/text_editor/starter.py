"""Implement TextEditor level by level. See README.md for the spec."""
from __future__ import annotations


class TextEditor:
    def __init__(self) -> None:
        pass  # TODO: design your Level 1 state here

    # --- Level 1 ---
    def insert(self, pos: int, text: str) -> None:
        raise NotImplementedError

    def delete(self, pos: int, length: int) -> None:
        raise NotImplementedError

    def get_text(self) -> str:
        raise NotImplementedError

    # --- Level 2 ---
    def undo(self) -> bool:
        raise NotImplementedError

    def redo(self) -> bool:
        raise NotImplementedError

    # --- Level 4 ---
    def set_cursor(self, pos: int) -> None:
        raise NotImplementedError

    def type_at_cursor(self, text: str) -> None:
        raise NotImplementedError

    def backspace_at_cursor(self, length: int) -> None:
        raise NotImplementedError


def test_level_1() -> None:
    editor = TextEditor()
    editor.insert(0, "hello")
    assert editor.get_text() == "hello"
    editor.insert(5, " world")
    assert editor.get_text() == "hello world"
    editor.delete(5, 6)
    assert editor.get_text() == "hello"


def test_level_2() -> None:
    editor = TextEditor()
    editor.insert(0, "hello")
    editor.insert(5, " world")
    assert editor.undo() is True
    assert editor.get_text() == "hello"
    assert editor.redo() is True
    assert editor.get_text() == "hello world"
    editor.insert(11, "!")
    assert editor.redo() is False  # new edit cleared the redo stack


def test_level_3_perf() -> None:
    import time

    editor = TextEditor()
    start = time.perf_counter()
    for i in range(3000):
        editor.insert(i, "x")
    elapsed = time.perf_counter() - start
    print(f"3000 inserts took {elapsed:.3f}s -- should stay well under a second")


if __name__ == "__main__":
    test_level_1()
    print("Level 1 OK")
    test_level_2()
    print("Level 2 OK")
    test_level_3_perf()
