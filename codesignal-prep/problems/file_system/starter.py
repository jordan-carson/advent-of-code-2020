"""Implement FileSystem level by level. See README.md for the spec."""
from __future__ import annotations


class FileSystem:
    def __init__(self) -> None:
        pass  # TODO: design your Level 1 state here (think tree vs. flat path map)

    # --- Level 1 ---
    def mkdir(self, path: str) -> bool:
        raise NotImplementedError

    def write_file(self, path: str, content: str) -> bool:
        raise NotImplementedError

    def read_file(self, path: str) -> str | None:
        raise NotImplementedError

    def list_dir(self, path: str) -> list[str] | None:
        raise NotImplementedError

    # --- Level 2 ---
    def set_permissions(self, path: str, owner: str, mode: str) -> bool:
        raise NotImplementedError

    # --- Level 3 ---
    def create_symlink(self, path: str, target: str) -> bool:
        raise NotImplementedError

    # --- Level 4 ---
    def mount(self, path: str, other_fs: "FileSystem") -> bool:
        raise NotImplementedError


def test_level_1() -> None:
    fs = FileSystem()
    assert fs.mkdir("/a/b") is True
    assert fs.write_file("/a/b/file.txt", "hello") is True
    assert fs.read_file("/a/b/file.txt") == "hello"
    assert fs.list_dir("/a/b") == ["file.txt"]
    assert fs.write_file("/missing/file.txt", "x") is False
    assert fs.read_file("/nope") is None


def test_level_2() -> None:
    fs = FileSystem()
    fs.mkdir("/a")
    fs.set_permissions("/a", owner="alice", mode="rw")
    fs.write_file("/a/f.txt", "content", as_user="alice")
    assert fs.write_file("/a/f.txt", "nope", as_user="bob") is False
    assert fs.read_file("/a/f.txt", as_user="bob") == "content"


def test_level_3() -> None:
    fs = FileSystem()
    fs.mkdir("/a")
    fs.write_file("/a/real.txt", "hi")
    assert fs.create_symlink("/link", "/a/real.txt") is True
    assert fs.read_file("/link") == "hi"
    fs.create_symlink("/x", "/y")
    assert fs.create_symlink("/y", "/x") is False  # would create a cycle


if __name__ == "__main__":
    test_level_1()
    print("Level 1 OK")
    test_level_2()
    print("Level 2 OK (adjust signatures to match your Level 2 design)")
    test_level_3()
    print("Level 3 OK")
