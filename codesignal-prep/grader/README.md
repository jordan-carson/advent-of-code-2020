# Auto-grader

Grades an attempt at any problem in `../problems/` (Python) or `../go/`
(Go) and reports a modeled score. Standard library only, same as the
practice problems themselves.

## What it's modeled on

Per public reports (candidate write-ups, aggregated on sites like
Glassdoor/Blind, and the spacecomplexity.ai phone-screen breakdown), the
real assessment:

- Uses CodeSignal's General Coding Framework: **one problem across four
  progressive levels**, all of whose tests are visible before you write
  that level's code.
- Scores on a **600-850 scale** (the floor and ceiling of CodeSignal's own
  scoring framework, not specific to this problem type).
- Grades on **correctness, code quality, and time efficiency** — not just
  whether the given tests go green.
- Anthropic's reported software-engineering cutoff is **~835/850** — about
  a 98% bar, with roughly 15 points of margin for error.

None of that is a leaked rubric. Anthropic hasn't published exact
per-level point values or the weighting between correctness/quality/time.
**This grader is a transparent, documented model calibrated to the two
concrete numbers above (the 600-850 scale and the ~835 cutoff) — treat its
output as practice feedback with the right shape and the right stakes, not
a prediction of your actual score.**

## The scoring model

```
score = 600 + 250 * (0.65 * correctness + 0.20 * quality + 0.15 * time)
```

- **Correctness (65%)** — per level, the fraction of that level's tests
  passing, weighted by level index (Level 4 is worth more than Level 1,
  proportional to `level / sum(1..N)` for the N levels a problem defines).
  This is the dominant term because a level that doesn't pass can't
  really be "well written" either.
- **Code quality (20%)** — static heuristics, not a style opinion: bare
  `except:`, wildcard imports, non-stdlib imports, oversized/overly
  branchy functions, `gofmt`/`go vet` failures, discarded Go errors, and
  (Go) an accidental external dependency in `go.mod`. Every deduction is
  named in the output. It deliberately does **not** penalize missing
  comments — the prep guidance is "default to no comments," and a quality
  checker that fights that would be self-defeating.
- **Time efficiency (15%)** — how quickly you actually cleared each level,
  against the budget in `../STRATEGY.md` (cumulative ~15 min/level after
  the 20-minute data-model stage). This is **only** measured if you ran
  `grade.py watch` during the attempt; otherwise it defaults to a neutral
  50%, which is why a perfect, clean solution graded with `score` alone
  tops out a few points under a perfect run (see the worked example
  below) — that gap *is* the "time efficiency" dimension the real rubric
  reportedly scores and this grader can't fabricate for you.

Weights are the one fully-invented part of this model — reweight them
yourself with `WEIGHTS` at the top of `grade.py` if you want to stress a
dimension harder.

## Usage

```bash
# see what's discoverable for every problem, both languages
python3 grade.py list

# grade one attempt in place (edits problems/<x>/starter.py or go/<x>/*.go directly)
python3 grade.py score --lang python --problem key_value_store
python3 grade.py score --lang go     --problem key_value_store

# grade a copy instead of the in-repo file
python3 grade.py score --lang python --problem key_value_store --file /path/to/attempt.py

# grade every problem for a language in one pass
python3 grade.py score --lang python --all

# capture real time-efficiency data: run this *while* you implement,
# start it the moment you start Level 1 (i.e. right after your 20-minute
# data-model stage). Ctrl+C when you're done for the session.
python3 grade.py watch --lang python --problem key_value_store
```

`watch` polls the target file's mtime, reruns the discovered tests on
every save, and the first time a level's tests all pass it records the
elapsed time since `watch` started into
`grader/.timing/<problem>.<lang>.json` (gitignored — it's a personal
practice log, not something to commit). The next `score` run for that
problem/language picks it up automatically.

## How levels and tests are found

The grader never hardcodes test names. It parses `problems/<x>/starter.py`
for top-level `def test_level_<N>...` functions (Python `ast`), and asks
`go test -list '.*'` for `TestLevel<N>...` functions in `go/<x>/`. A
problem can have multiple test functions per level (e.g.
`package_manager`'s `test_level_1_linear`/`_cycle`/`_diamond`) — they're
grouped and averaged within that level. Not every problem's starter has
tests written for all 4 levels yet (`package_manager` only has Level 1,
for instance) — the grader scores whatever levels it finds and says so;
scores aren't comparable across problems with different level counts.

Each test runs in its own subprocess (Python) or its own `go test -run
'^Name$'` invocation (Go), with a timeout (default 5s, `--timeout` to
change it). That isolation matters: a `panic`/uncaught exception in one
level's implementation only fails that level's test, instead of crashing
the whole grading run the way an unrecovered panic would crash a single
`go test ./...` invocation.

## Worked example

Implementing all four `key_value_store` levels correctly (no bugs, no
quality smells) and grading with plain `score` (no `watch` log) reports
**831/850** — 4 points under the modeled cutoff, entirely because time
efficiency defaults to neutral. Run the same attempt under `watch` and
finish each level inside its budget, and the same code clears 850. That
gap is the point: correctness alone gets you close, but the reported
~15-point margin for error is exactly where an untimed "I got the tests
green eventually" attempt falls short.
