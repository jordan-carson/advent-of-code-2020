# Concurrency drills

Ten small, isolated packages, one per primitive. This is a different kind
of practice than `../keyvaluestore`, `../ratelimiter`, etc.: those are
whole leveled systems (and the only thing `../../grader/` scores);
these are the tools those systems' stretch levels quietly assume you
already have — `build_system`'s Level 4 parallelism, `web_crawler`'s
Level 4 distributed simulation, and any thread-safe version of
`rate_limiter` or `key_value_store` you'd actually deploy. Ungraded,
correctness-only, no solutions.

No solution code here on purpose — fill in each `panic("not implemented")`
yourself. Run everything with the race detector; it's the single most
useful tool for this kind of code:

```bash
go test -race ./concurrency/...
```

## Order and what each one drills

1. **`goroutines/`** — spawn one goroutine per unit of work, know when
   they're all done, without any of the sync package yet (a plain channel
   as the completion signal). The warm-up.
2. **`channels/`** — the pipeline-stage contract: close your output
   channel once your input is drained, exactly once, so stages compose.
3. **`bufferedchannels/`** — a buffered channel *is* a bounded,
   concurrency-safe FIFO queue: `Push` blocks when full, `Pop` blocks
   when empty, for free.
4. **`select/`** — merge multiple channels (fan-in), and race a receive
   against a timeout (`select` + `time.After`).
5. **`waitgroup/`** — `sync.WaitGroup` is what `goroutines/`'s manual
   channel-signal pattern turns into once you don't need to move data
   through the channel, only a "done" signal. Classic bug: call `Add`
   before `go`, never inside the goroutine.
6. **`mutex/`** — `sync.Mutex`: make a shared map safe by making every
   operation exclusive. The test that matters is the concurrent-hammer
   one, run with `-race`.
7. **`rwmutex/`** — `sync.RWMutex`: let concurrent reads through, still
   exclude writers. After it passes, benchmark it against `mutex/`'s
   equivalent (`go test -bench=. -run=^$ -cpu=4` in each) — on this
   machine a correct RWMutex `Get` ran ~2.5x faster than the Mutex
   version under a read-only load. That gap is the whole reason the type
   exists.
8. **`once/`** — `sync.Once`: lazy init that runs exactly once no matter
   how many goroutines race to trigger it first. The test sleeps inside
   the load function specifically to widen the race window, so a naive
   "if not loaded yet" check (without `sync.Once`) gets caught loading
   twice.
9. **`context/`** — `context.Context`'s two canonical shapes: race real
   work against a deadline/cancellation (`select` on a result channel vs.
   `ctx.Done()`), and a loop that checks `ctx.Done()` every tick instead
   of running to some fixed limit.
10. **`ownership/`** — ties it together: the same counter implemented
    both ways, mutex-guarded shared state vs. a single owning goroutine
    reached only through channel messages ("don't communicate by sharing
    memory; share memory by communicating"). Do this one last — it's
    easiest to appreciate once `mutex/`, `channels/`, and `select/` are
    already second nature.

## Where these actually get used

Go back to `../../problems/*/README.md` stretch levels once these pass:
- `build_system` Level 4 (parallelism) is `waitgroup/` + `goroutines/`
  applied to a DAG scheduler.
- `web_crawler` Level 4 (simulated distributed crawling) is
  `bufferedchannels/` (a shared frontier queue) + `waitgroup/` (worker
  pool) + `mutex/` or `ownership/` (the visited-set).
- A real (not simulated-`now`) `rate_limiter` or `key_value_store` needs
  `mutex/` or `rwmutex/` around its state, and `context/` for
  cancellation on the calls that use it.

These primitives aren't wired into those problems' starters — the
systems track keeps `now`/`sleep` injected and single-threaded so it stays
deterministic for the grader. Once you're comfortable here, rewriting one
of those stretch levels to be genuinely concurrent (real goroutines, real
`time.Now()`, a real worker pool) is a good next drill in its own right.
