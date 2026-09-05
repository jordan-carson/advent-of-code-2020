# Operating framework

## Assume six stages, not four

The confirmed format escalates across four levels, but treat every session
as if two more waves are coming after the ones you can see — because on the
real assessment, further requirements are revealed only after you clear the
current level, and the safest assumption is that they will keep coming.
Budget time and structure accordingly:

| Time | Stage | What you're doing |
|---|---|---|
| 0:00–0:20 | Data model | No feature code yet. Decide the core entities, what state lives where, and what's immutable vs. mutable. |
| 0:20–0:35 | Level 1 | Implement + pass the given tests. |
| 0:35–0:50 | Level 2 | Extend, don't rewrite. |
| 0:50–1:05 | Level 3 | Extend again. This is usually where time-dependent or filtering logic shows up. |
| 1:05–1:20 | Level 4 | Persistence/compression/conflict-resolution-shaped complexity. |
| 1:20–1:30 | Buffer / stretch | Either finish Level 4 edge cases, or — if you're ahead — sketch what a Level 5 would need and confirm your structures wouldn't break. |

If a real screen only has four levels, finishing early with buffer time is
a good outcome. If it has more, you're already paced for it.

## The twenty-minute data model check

Before writing any feature logic, ask one question: **if a stranger handed
me a requirement I cannot see right now, would my structure bend or break?**

Concretely, before Level 1 code:

- What are the nouns? (e.g., for a KV store: `key`, `value`, `record` —
  where `record` might carry metadata like expiry or version even if
  Level 1 doesn't need it yet.)
- Where does state live — one dict, or does it already smell like it needs
  an index, a queue, or a tree? Don't build the tree yet; just don't choose
  a shape that forecloses one.
- What's the seam where "one more requirement" is most likely to land?
  (TTL on a KV store, permissions on a filesystem, interest on a bank
  account.) Leave that seam open — an extra field, a method that currently
  has one branch — without speculatively implementing the feature itself.

This is not "build for the future" in the sense of premature abstraction.
It's the opposite: pick the plainest structure that doesn't have to be torn
up when the next level's requirement lands. Concretely this usually means:
wrap primitive values in a small record/dataclass from Level 1 even when a
raw value would pass Level 1's tests, because Level 3 almost always wants
to attach metadata to that value.

## Practice by building systems end to end, not memorizing problems

Drill: build one of the systems in `problems/` cold, with no reference to a
prior attempt. Once Level 1–4 pass, bolt on a feature you did not plan for
(invent one, or ask someone else to name one). That "unplanned feature"
step is the actual muscle being tested — not the algorithm, the shape of
the code that has to absorb it.

Do this without AI assistance. The assessment is you, alone, extending your
own code under time pressure; practicing any other way doesn't train that.

## Writing your own tests

Given tests only confirm the requirements you were told about. Before
calling a level "done," write one or two tests of your own that a careless
reading of the spec would miss — an empty input, a duplicate key, a
zero-or-negative TTL, an operation on a deleted account. Anthropic's
scoring reportedly looks at whether your solution generalizes, not just
whether the given tests are green — the same discipline that write-your-
own-tests habit builds is what carries into the next level's hidden edge
cases.

## Common mistakes

- **Solving Level 1 as if it's the whole problem.** Hardcoding return types,
  overfitting to the exact given tests, or picking a data structure that's
  only efficient for the Level 1 operations.
- **Rewriting instead of extending.** If Level 2 requires touching more than
  the seam you left open in Level 1, that's a signal your Level 1 model was
  too narrow — don't paper over it, fix the model even if it costs a few
  minutes.
- **No time left for Level 3/4 because Level 1/2 were gold-plated.** Time-box
  each stage; a passing-but-plain solution beats an elegant one that never
  got submitted.
- **Skipping the read-all-tests-first step.** Every level's tests are visible
  before you write code for it — read all of them before writing anything,
  since they define the contract more precisely than the prose does.
