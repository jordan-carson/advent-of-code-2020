# Package manager

Implement `PackageManager` in `starter.py`. Tests dependency-graph
reasoning, version constraints, and conflict resolution.

## Level 1 — install / dependency resolution
- `add_package(name: str, version: str, dependencies: list[str] = []) ->
  None` — registers a version of a package, with hard dependency names
  (no version constraint yet — assume exactly one version of each package
  is ever registered at this level)
- `install(name: str) -> list[str] | None` — returns the install order
  (dependencies before dependents, topologically sorted) or `None` if a
  dependency cycle exists

## Level 2 — multiple versions
- `add_package(name, version, dependencies)` can now be called multiple
  times for the same `name` with different `version`s
- `install(name: str, version: str) -> list[str] | None`

## Level 3 — version constraints
- Dependencies are now `(name, constraint)` pairs, e.g. `("lib", ">=1.0,
  <2.0")`. `install` must pick, for each dependency, a registered version
  satisfying the constraint (prefer the highest satisfying version),
  or return `None` if none satisfies it

## Level 4 — conflict resolution
- If two different packages in the resolved graph require incompatible
  versions of the same dependency (no single version satisfies both
  constraints), `install` returns `None`. Otherwise, resolve to one
  version per package across the whole graph, even if requested by
  multiple paths.

## Level 5 (stretch) — uninstall with reference counting
- `uninstall(name: str, version: str) -> bool` — only actually removes a
  package if nothing else currently installed depends on it

## Level 6 (stretch) — lockfile diffing
- `diff(old_lockfile: dict, new_lockfile: dict) -> dict` — returns which
  packages were added, removed, or changed version between two install
  results
