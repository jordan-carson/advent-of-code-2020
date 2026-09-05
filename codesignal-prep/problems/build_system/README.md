# Build system

Implement `BuildSystem` in `starter.py`. Tests DAG scheduling, caching,
and parallelism reasoning.

## Level 1 — task scheduling
- `add_task(name: str, dependencies: list[str] = []) -> None`
- `build_order(target: str) -> list[str] | None` — a valid topological
  order to build `target` and everything it (transitively) depends on, or
  `None` on a cycle

## Level 2 — DAG execution
- `run(target: str, executor: Callable[[str], None]) -> list[str]` —
  actually calls `executor(task_name)` for each task in a valid dependency
  order, returns the order it executed in

## Level 3 — caching
- `mark_dirty(name: str) -> None` — invalidates a task and everything that
  transitively depends on it
- `run(target, executor)` now only calls `executor` for dirty tasks
  (everything starts dirty the first time); tasks not (transitively)
  affected by a `mark_dirty` call are skipped on the next `run`

## Level 4 — parallelism
- `run_parallel(target: str, executor, max_workers: int) -> list[str]` —
  tasks with no unmet dependency can run concurrently (a real thread pool
  is fine, or a simulated round-based scheduler — document which); returns
  a valid dependency-respecting order tasks *started* in

## Level 5 (stretch) — task outputs feeding inputs
- `add_task(name, dependencies, executor)` where `executor` receives a
  dict of `{dependency_name: its_return_value}` and its own return value
  becomes available to dependents

## Level 6 (stretch) — partial rebuild diffing
- `affected_by(name: str) -> list[str]` — everything that would be
  rebuilt if `name` changed, without actually running the build
