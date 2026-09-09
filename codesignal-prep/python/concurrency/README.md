# Concurrency drills (Python)

The Python translation of `../../go/concurrency/` — same ten primitives,
same purpose: prerequisites for the systems track's concurrency-shaped
stretch levels (`build_system` Level 4 parallelism, `web_crawler` Level 4
distributed crawling), not one of the leveled systems `../../grader/`
scores. Ungraded, correctness-only, no solutions.

## Terminology map (Go → Python)

| Go | Python here | Notes |
|---|---|---|
| goroutine | `threading.Thread` | A real OS thread, not a lightweight green one -- heavier to spawn thousands of, same fan-out/fan-in shape |
| channel (unbuffered) | `queue.Queue` + a `SENTINEL` for "closed" | No true zero-capacity/rendezvous channel in the stdlib; queues have no `close()` |
| buffered channel | `queue.Queue(maxsize=N)` | Exact match — blocks on full/empty for free |
| `select` | polling loop over `get_nowait()`, or one shared queue | No stdlib "wait on any of several queues"; see `select/` |
| `sync.WaitGroup` | hand-built `WaitGroup` (Condition + counter) | No stdlib equivalent — `Thread.join()` covers the simple case, building this teaches the pattern underneath it |
| `sync.Mutex` | `threading.Lock` | Exact match |
| `sync.RWMutex` | hand-built `ReadWriteLock` | No stdlib equivalent at all |
| `sync.Once` | hand-built `Once` | No stdlib equivalent |
| `context.Context` | hand-built `CancelContext` | No stdlib equivalent for plain threads (asyncio has its own, different, cooperative story) |

Four of these (`WaitGroup`, `RWMutex`, `Once`, `Context`) don't exist in
Python's standard library at all — you're building the primitive itself,
not just using a stdlib class. That's not a workaround, it's most of the
point: it's the same reason these show up in interviews in the first
place.

## Two honest caveats

**No `-race`.** Go's race detector is a dynamic, instrumented checker
that catches a data race the instant it happens. Python has nothing
equivalent for plain threads. Every "does this race?" test here is a
*statistical* stress test — it hammers shared state hard enough that a
broken implementation is very likely to lose an update, not certain to.
Passing is meaningful evidence, not proof. Where a test needed real
tuning to be reliable (`mutex/`, `ownership/`), it's `sys.setswitchinterval()`
forcing much more frequent thread switches than CPython's 5ms default —
still empirically verified against a known-broken implementation, just
verified statistically rather than by instrumentation.

**The GIL changes what "concurrent" buys you.** Go goroutines run on real
OS threads with true parallelism; CPython threads only run Python
bytecode one at a time no matter how many you spawn. Concretely: `rwmutex/`'s
benchmark shows a plain `Mutex` *beating* the hand-built `RWLock` for a
pure in-memory dict lookup (there's no real parallelism to win back, and
the Condition-based bookkeeping costs more than a bare `Lock`) — the
RWLock only wins once the protected work actually releases the GIL (real
I/O, or a C extension). That's the opposite of the Go version's result,
and it's a real, useful thing to know, not a flaw in the exercise.

## Order and what each one drills

1. **`threads/`** — spawn one thread per unit of work, know when they're
   all done, with nothing but a list to `join()`. The warm-up.
2. **`channels/`** — the pipeline-stage contract translated to queues: put
   a `SENTINEL` on your output once your input is drained and exhausted,
   exactly once, so stages compose.
3. **`bufferedchannels/`** — `queue.Queue(maxsize=N)` already gives you a
   bounded, thread-safe FIFO for free; this is about using it (and its
   non-blocking `_nowait` variants) correctly.
4. **`select/`** — merge multiple queues (fan-in), and race a receive
   against a timeout via polling, since Python has no native multi-queue
   wait.
5. **`waitgroup/`** — build the `Add`/`Done`/`Wait` pattern from a
   `Condition`. Same footgun as Go: call `add()` before starting the
   thread, never from inside it.
6. **`mutex/`** — `threading.Lock` guarding a shared dict. The test that
   matters is the concurrent-hammer one; read the module docstring for
   why it deliberately uses `dict.get()` rather than a plain attribute.
7. **`rwmutex/`** — build a `ReadWriteLock` from a `Condition` + reader
   count, then run `benchmark.py` and see the GIL caveat above land for
   real, not just as a warning.
8. **`once/`** — build `Once`'s exactly-once-under-a-race guarantee. The
   test sleeps inside the load function specifically to widen the race
   window, so a naive "if not loaded yet" check gets caught loading
   twice — verified empirically against a broken version during this
   exercise's own construction.
9. **`context/`** — `CancelContext`'s two canonical uses: race real work
   against a deadline, and a loop that checks for cancellation every
   tick instead of running forever.
10. **`ownership/`** — the same counter twice: `Lock`-guarded shared
    state vs. one thread owning the value, reached only through a
    `queue.Queue` of commands. Do this one last.

## Running the exercises

Each directory is standalone (no shared `__init__.py`/package structure —
matching the flat, no-framework style the rest of `codesignal-prep/`
already uses). From inside a directory:

```bash
python3 test_<name>.py
```

Every test file is runnable directly (plain `assert`-based functions
called from `__main__`, same convention as `problems/*/starter.py`) —
no `pytest` or other dependency needed.
