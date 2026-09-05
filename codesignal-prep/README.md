# CodeSignal Prep (Anthropic-style progressive assessment)

This folder is a self-contained practice area. It has nothing to do with the
Advent of Code solutions elsewhere in this repo — it exists purely to drill
the specific skill Anthropic's CodeSignal screen tests: **building a system
whose architecture survives requirements you haven't seen yet.**

Do the practice runs yourself, without AI assistance. The whole point of the
exercise is to train the design instinct under time pressure; leaning on a
model while practicing trains a muscle you won't have in the room. Use this
folder only as a scaffold — the problem statements and empty stubs — not as
a place to get answers.

## Read first

- `STRATEGY.md` — the operating framework: how to spend the 90 minutes,
  the "would this bend or break" data-model check, and the mistakes that
  sink otherwise-strong candidates.
- `timer.py` — a stdlib-only staged timer that mirrors the assessment's
  time pressure across six stages instead of four.

## How to run a practice session

1. Pick one system from `problems/` (don't reread it if you've drilled it
   recently — the goal is repeated cold starts, not memorized answers).
2. Start the timer: `python3 timer.py`.
3. Open only that problem's `README.md` and `starter.py`. Implement Level 1
   directly in `starter.py`, run your own tests, then move to Level 2, and
   so on — without rewriting what already works.
4. When you hit the end of the listed levels, keep going: invent your own
   Level 5/6 extension in the same spirit as the ones before it. That's the
   "assume two more waves are coming" habit — build for it before you're
   forced to.
5. Afterward, do a 5-minute postmortem: which of your Level 1 decisions had
   to be undone later? That's the tell for what to fix next time.

## Systems included

| System | Core theme |
|---|---|
| `key_value_store` | data structure + expiry + snapshotting |
| `banking_system` | transactional integrity, time-dependent state |
| `file_system` | hierarchical modeling, permission inheritance |
| `rate_limiter` | sliding windows, per-key state, concurrency-shaped bugs |
| `package_manager` | dependency graphs, version constraints, conflicts |
| `build_system` | DAG scheduling, caching, parallelism |
| `text_editor` | undo/redo, efficient text representations |
| `web_crawler` | fetch/parse pipelines, rate limiting, dedup at scale |

Constraints to practice under, matching the real assessment: Python only,
standard library only (no pip installs), and you can see all the tests for
a level before writing code for it — so read every test in a level before
touching the implementation.
