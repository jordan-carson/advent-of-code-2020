# Rate limiter

Implement `RateLimiter` in `starter.py`. Tests sliding-window logic,
per-key state, and the kind of subtle bugs that show up under concurrency
even in single-threaded simulations (off-by-one window edges, stale state).

All time values are passed in explicitly as `now` (a float, seconds) —
don't call `time.time()` yourself, so tests stay deterministic.

## Level 1 — fixed window
- `allow(client_id: str, now: float) -> bool` — allow up to `limit`
  requests (constructor arg) per fixed `window_seconds` (constructor arg)
  window per client; window boundaries align to `window_seconds`
  multiples of epoch time

## Level 2 — sliding window
- `allow_sliding(client_id: str, now: float) -> bool` — same limit, but
  using a true sliding window (count requests within the last
  `window_seconds`, not a fixed bucket)

## Level 3 — per-client custom limits
- `set_limit(client_id: str, limit: int, window_seconds: float) -> None`
  overrides the default limit/window for one client; unconfigured clients
  keep using the constructor defaults

## Level 4 — burst allowance (token bucket)
- `allow_bucket(client_id: str, now: float, cost: int = 1) -> bool` — a
  token-bucket variant where tokens refill continuously at
  `limit / window_seconds` tokens/sec up to a max capacity, and a request
  can cost more than one token

## Level 5 (stretch) — priority tiers
- `allow(client_id, now, priority: str = "normal")` — a `"high"` priority
  request may borrow from a small reserved pool even when the normal pool
  is exhausted

## Level 6 (stretch) — distributed accounting
- `merge(other: "RateLimiter") -> None` — combine request counts from
  another instance's window state as if requests had been interleaved
  across two nodes sharing the same limits
