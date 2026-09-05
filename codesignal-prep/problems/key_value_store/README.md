# In-memory key-value store

The most frequently reported Anthropic CodeSignal problem. Implement
`KeyValueStore` in `starter.py`. Levels 1-4 mirror the reported format;
5-6 are stretch levels to practice for "more waves than you expect."

Read every level's tests before writing that level's code.

## Level 1 — basic operations
- `set(key: str, value: str) -> None`
- `get(key: str) -> str | None` — `None` if missing
- `delete(key: str) -> bool` — returns whether something was deleted

## Level 2 — filtered scans and range queries
- `scan(prefix: str) -> list[str]` — all keys starting with `prefix`,
  sorted ascending
- `scan_range(start: str, end: str) -> list[str]` — all keys `start <= key
  <= end`, sorted ascending

## Level 3 — TTL (time-to-live) expiration
- `set_with_ttl(key: str, value: str, ttl_seconds: float) -> None`
- `get` must return `None` for an expired key (and should treat it as
  deleted — don't let it show up in `scan`/`scan_range` either)
- Think about whether expiry is checked lazily (on read) or needs active
  cleanup, and what that implies for `scan`'s cost

## Level 4 — snapshotting / persistence
- `snapshot() -> dict` — a serializable snapshot of current live (non
  -expired) state
- `restore(snapshot: dict) -> None` — replace current state with a
  previously captured snapshot
- Decide what "restore" does to TTLs — do restored keys keep their
  original expiry, get a fresh one, or become permanent? Pick one and be
  consistent; state your assumption in a comment if it's not obvious from
  the tests.

## Level 5 (stretch) — transactions
- `begin() -> None`, `commit() -> None`, `rollback() -> None`
- Writes inside a transaction aren't visible to `get`/`scan` until commit;
  `rollback` discards them entirely. No nested transactions required.

## Level 6 (stretch) — namespaces
- Every operation optionally takes a `namespace: str = "default"` and
  keys in different namespaces never collide, including in `snapshot`
  /`restore`.
