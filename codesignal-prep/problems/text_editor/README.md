# Text editor

Implement `TextEditor` in `starter.py`. Tests undo/redo design and
efficient text representations.

## Level 1 — insert / delete
- `insert(pos: int, text: str) -> None`
- `delete(pos: int, length: int) -> None`
- `get_text() -> str`

## Level 2 — undo / redo
- `undo() -> bool` — reverts the last insert/delete, returns whether
  there was anything to undo
- `redo() -> bool` — reapplies the last undone operation; any new edit
  after an undo clears the redo stack

## Level 3 — efficient representation
- Same operations, but they must stay reasonably fast on large documents
  with many small edits (this is the "rope data structure" territory
  mentioned in reports — a naive `str` rebuild per edit is the thing to
  move away from; a piece table or a simple balanced structure both work).
  Prove it to yourself: write a quick timing check with a few thousand
  small inserts and see if performance stays roughly linear in edit count
  rather than growing quadratically with document size

## Level 4 — cursor-relative operations
- `set_cursor(pos: int) -> None`
- `type_at_cursor(text: str) -> None`, `backspace_at_cursor(length: int) ->
  None` — cursor advances/retreats with the edit, and undo/redo restore
  cursor position too

## Level 5 (stretch) — named snapshots
- `save_snapshot(name: str) -> None`, `restore_snapshot(name: str) ->
  bool` — independent of the undo/redo stack

## Level 6 (stretch) — collaborative editing
- `apply_remote_edit(op: dict) -> None` — apply an edit that arrived from
  another editor's operation log, transforming it against any local edits
  that happened concurrently (a basic operational-transform sketch is
  enough — this one is intentionally open-ended)
