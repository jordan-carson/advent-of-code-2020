# File system simulator

Implement `FileSystem` in `starter.py`. Tests hierarchical data modeling
and edge cases around permissions and circular references.

Paths are absolute, `/`-separated, root is `/`.

## Level 1 — create and read
- `mkdir(path: str) -> bool` — creates all missing intermediate
  directories (like `mkdir -p`); `False` if `path` already exists as a file
- `write_file(path: str, content: str) -> bool` — parent dir must exist
- `read_file(path: str) -> str | None`
- `list_dir(path: str) -> list[str] | None` — sorted immediate children

## Level 2 — permissions
- `set_permissions(path: str, owner: str, mode: str) -> bool` — `mode` is
  one of `"r"`, `"rw"`
- `read_file(path, as_user)` / `write_file(path, content, as_user)` now
  take a `as_user` argument and must respect the owning user's mode
  (non-owners get read-only regardless of mode, for this exercise — pick
  and document your own permission model, the point is being consistent)
- New files/dirs inherit permissions from their parent directory at
  creation time

## Level 3 — symlinks
- `create_symlink(path: str, target: str) -> bool`
- Reads/writes/listings through a symlink resolve to the target
- Detect and reject symlink cycles (`A -> B -> A`) instead of infinite
  looping

## Level 4 — mounting
- `mount(path: str, other_fs: "FileSystem") -> bool` — grafts another
  `FileSystem` instance's root onto `path` in this one; operations under
  `path` should transparently delegate to `other_fs`

## Level 5 (stretch) — quotas
- `set_quota(path: str, max_bytes: int) -> None` — writes under `path`
  that would exceed the cumulative quota fail without partial writes

## Level 6 (stretch) — move/copy with history
- `move(src: str, dst: str) -> bool`, `copy(src: str, dst: str) -> bool`
  (recursive for directories), and a `history(path) -> list[str]` of
  operations that touched a given path or its descendants
