#!/usr/bin/env python3
"""Auto-grader for the codesignal-prep practice problems.

Models Anthropic's reported CodeSignal General Coding Framework scoring:
a 600-850 scale, correctness + code quality + time efficiency, with a
~835/850 reported cutoff for software engineering roles. The exact
per-dimension weights and per-level point values are NOT published --
the formula here (see WEIGHTS / level_weight_fractions below) is a
documented, transparent model calibrated to those two known numbers, not
a verified replica. Treat the score as directional practice feedback, not
a promise about the real assessment. See ../grader/README.md for the
full explanation of what's modeled and what isn't.

Usage:
    python3 grade.py list
    python3 grade.py score --lang python --problem key_value_store
    python3 grade.py score --lang go --problem key_value_store
    python3 grade.py score --lang python --all
    python3 grade.py watch --lang python --problem key_value_store

Standard library only.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREP_ROOT = HERE.parent
GO_ROOT = PREP_ROOT / "go"

# Python problem dir name -> Go package dir name (Go package names drop
# underscores; see codesignal-prep/README.md).
PROBLEM_DIRS = {
    "key_value_store": "keyvaluestore",
    "banking_system": "bankingsystem",
    "file_system": "filesystem",
    "rate_limiter": "ratelimiter",
    "package_manager": "packagemanager",
    "build_system": "buildsystem",
    "text_editor": "texteditor",
    "web_crawler": "webcrawler",
}

# Modeled composite weights. Correctness dominates because it gates
# advancement most directly (a level that doesn't pass can't be "well
# written"); quality and time are secondary signals the reported rubric
# names but doesn't weight publicly.
WEIGHTS = {"correctness": 0.65, "quality": 0.20, "time": 0.15}

SCALE_MIN, SCALE_MAX = 600, 850
REPORTED_CUTOFF = 835

# Cumulative minutes-from-start-of-implementation a level should be fully
# passing by, per STRATEGY.md's stage budget (20 min data model, then ~15
# min per level). Stretch levels 5/6 get +10 min each. Only used by the
# time-efficiency score, and only if a `watch` session logged real timings.
CUMULATIVE_BUDGET_MINUTES = {1: 15, 2: 30, 3: 45, 4: 60, 5: 70, 6: 80}

TEST_TIMEOUT_SECONDS = 5.0


# --------------------------------------------------------------------------
# Discovery: find test_level_N (Python) / TestLevelN (Go) functions so the
# grader never needs a hand-maintained list of test names per problem.
# --------------------------------------------------------------------------

def discover_python_tests(file_path: Path) -> dict[int, list[str]]:
    tree = ast.parse(file_path.read_text())
    levels: dict[int, list[str]] = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            m = re.match(r"test_level_(\d+)", node.name)
            if m:
                levels.setdefault(int(m.group(1)), []).append(node.name)
    return levels


def discover_go_tests(pkg_name: str) -> dict[int, list[str]]:
    proc = subprocess.run(
        ["go", "test", "-list", ".*", f"./{pkg_name}"],
        cwd=GO_ROOT, capture_output=True, text=True, timeout=60,
    )
    levels: dict[int, list[str]] = {}
    for line in proc.stdout.splitlines():
        line = line.strip()
        m = re.match(r"TestLevel(\d+)", line)
        if m:
            levels.setdefault(int(m.group(1)), []).append(line)
    return levels


# --------------------------------------------------------------------------
# Running individual tests in isolation, so one crash/panic only fails that
# one test instead of silently swallowing every test after it.
# --------------------------------------------------------------------------

def run_python_test(file_path: Path, test_name: str, timeout: float) -> tuple[bool, float, str]:
    script = (
        "import importlib.util\n"
        f"spec = importlib.util.spec_from_file_location('attempt', {str(file_path)!r})\n"
        "mod = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(mod)\n"
        f"getattr(mod, {test_name!r})()\n"
    )
    start = time.monotonic()
    try:
        proc = subprocess.run(
            [sys.executable, "-c", script], capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return False, timeout, f"TIMEOUT after {timeout}s (possible infinite loop)"
    elapsed = time.monotonic() - start
    if proc.returncode == 0:
        return True, elapsed, ""
    stderr_lines = [l for l in proc.stderr.strip().splitlines() if l.strip()]
    detail = stderr_lines[-1] if stderr_lines else f"exited {proc.returncode}"
    return False, elapsed, detail


def run_go_test(pkg_name: str, test_name: str, timeout: float) -> tuple[bool, float, str]:
    start = time.monotonic()
    try:
        proc = subprocess.run(
            ["go", "test", "-run", f"^{test_name}$", f"-timeout={timeout}s", "-v", f"./{pkg_name}"],
            cwd=GO_ROOT, capture_output=True, text=True, timeout=timeout + 30,
        )
    except subprocess.TimeoutExpired:
        return False, timeout, f"TIMEOUT after {timeout}s"
    elapsed = time.monotonic() - start
    if proc.returncode == 0:
        return True, elapsed, ""
    combined = (proc.stdout + proc.stderr).strip().splitlines()
    meaningful = [l for l in combined if l.strip() and not l.startswith("=== RUN") and not l.startswith("--- FAIL")]
    detail = meaningful[-1] if meaningful else (combined[-1] if combined else "failed")
    return False, elapsed, detail


def run_all_tests(problem: str, lang: str, file_or_pkg, levels: dict[int, list[str]], timeout: float):
    """Returns (results, details): results[level] = [bool,...], details[level] = [(name, msg),...] for failures."""
    results: dict[int, list[bool]] = {}
    details: dict[int, list[tuple[str, str]]] = {}
    for lvl, names in sorted(levels.items()):
        results[lvl] = []
        for name in names:
            if lang == "python":
                passed, _elapsed, detail = run_python_test(file_or_pkg, name, timeout)
            else:
                passed, _elapsed, detail = run_go_test(file_or_pkg, name, timeout)
            results[lvl].append(passed)
            if not passed:
                details.setdefault(lvl, []).append((name, detail))
    return results, details


# --------------------------------------------------------------------------
# Correctness scoring: later levels are worth more, proportional to their
# level index, normalized so the levels present always sum to 1.0 -- this
# keeps problems with different numbers of defined levels comparable.
# --------------------------------------------------------------------------

def level_weight_fractions(levels: list[int]) -> dict[int, float]:
    levels_sorted = sorted(levels)
    n = len(levels_sorted)
    denom = n * (n + 1) / 2
    return {lvl: (i + 1) / denom for i, lvl in enumerate(levels_sorted)}


def score_correctness(results: dict[int, list[bool]]) -> tuple[float, dict[int, dict]]:
    fracs = level_weight_fractions(list(results))
    total = 0.0
    breakdown = {}
    for lvl, passes in results.items():
        pass_frac = (sum(passes) / len(passes)) if passes else 0.0
        contribution = fracs[lvl] * pass_frac
        total += contribution
        breakdown[lvl] = {
            "passed": sum(passes), "of": len(passes),
            "weight": fracs[lvl], "contribution": contribution,
        }
    return total, breakdown


# --------------------------------------------------------------------------
# Code quality: transparent static heuristics, not a black box. Every
# deduction is named so you can see exactly why the score moved. These are
# deliberately conservative -- they flag real smells (bare except, ignored
# errors, wildcard imports, non-stdlib imports, oversized/branchy
# functions) and nothing about *style* (naming, comments) since the prep
# guidance is "default to no comments," which a quality checker shouldn't
# contradict.
# --------------------------------------------------------------------------

def assess_python_quality(source: str) -> tuple[float, list[str]]:
    score = 1.0
    findings: list[str] = []
    tree = ast.parse(source)

    if any(isinstance(n, ast.ExceptHandler) and n.type is None for n in ast.walk(tree)):
        score -= 0.15
        findings.append("bare `except:` clause -- silently swallows errors")

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and any(a.name == "*" for a in node.names):
            score -= 0.1
            findings.append(f"`from {node.module} import *` -- avoid wildcard imports")

    stdlib = getattr(sys, "stdlib_module_names", frozenset())
    for node in ast.walk(tree):
        mods = []
        if isinstance(node, ast.Import):
            mods = [a.name.split(".")[0] for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            mods = [node.module.split(".")[0]]
        for m in mods:
            if stdlib and m not in stdlib:
                score -= 0.1
                findings.append(f"non-stdlib import `{m}` -- the real assessment is Python-stdlib-only")

    branch_types = (ast.If, ast.For, ast.While, ast.Try, ast.BoolOp)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            length = (node.end_lineno or node.lineno) - node.lineno
            if length > 40:
                score -= 0.05
                findings.append(f"`{node.name}` is {length} lines -- consider splitting it up")
            branches = sum(1 for n in ast.walk(node) if isinstance(n, branch_types))
            if branches > 12:
                score -= 0.1
                findings.append(f"`{node.name}` has ~{branches} branch points -- high complexity for one function")

    return max(score, 0.0), findings


def assess_go_quality(pkg_name: str) -> tuple[float, list[str]]:
    score = 1.0
    findings: list[str] = []
    pkg_dir = GO_ROOT / pkg_name

    fmt_out = subprocess.run(["gofmt", "-l", "."], cwd=pkg_dir, capture_output=True, text=True)
    if fmt_out.stdout.strip():
        score -= 0.15
        findings.append("gofmt reports unformatted files -- run `gofmt -w .`")

    vet_out = subprocess.run(["go", "vet", f"./{pkg_name}"], cwd=GO_ROOT, capture_output=True, text=True)
    if vet_out.returncode != 0:
        score -= 0.3
        findings.append("`go vet` failed:\n" + vet_out.stderr.strip())

    for go_file in sorted(pkg_dir.glob("*.go")):
        if go_file.name.endswith("_test.go"):
            continue
        text = go_file.read_text()
        if re.search(r"\b_\s*=\s*err\b", text):
            score -= 0.1
            findings.append(f"{go_file.name}: an error is explicitly discarded (`_ = err`)")

    mod_text = (GO_ROOT / "go.mod").read_text()
    if re.search(r"^require\b", mod_text, flags=re.MULTILINE):
        score -= 0.2
        findings.append("go.mod has a `require` -- the real assessment is Go-stdlib-only")

    return max(score, 0.0), findings


# --------------------------------------------------------------------------
# Time efficiency: only scored if a `watch` session recorded real
# level-clearing timestamps (see cmd_watch). Otherwise neutral 0.5.
# --------------------------------------------------------------------------

def timing_log_path(problem: str, lang: str) -> Path:
    return HERE / ".timing" / f"{problem}.{lang}.json"


def load_timing_log(problem: str, lang: str) -> dict[int, float]:
    path = timing_log_path(problem, lang)
    if not path.exists():
        return {}
    raw = json.loads(path.read_text())
    return {int(k): v for k, v in raw.items()}


def score_time(cleared: dict[int, float], levels_present: list[int]) -> tuple[float, list[str]]:
    if not cleared:
        return 0.5, ["no timing log found -- run `grade.py watch ...` during a real attempt "
                      "to score this dimension for real; defaulted to neutral 0.5"]
    fracs = level_weight_fractions(levels_present)
    total = 0.0
    findings = []
    for lvl in levels_present:
        budget_s = CUMULATIVE_BUDGET_MINUTES.get(lvl, 15 * lvl) * 60
        if lvl in cleared:
            ratio = cleared[lvl] / budget_s
            sub = max(0.0, min(1.0, 2.0 - ratio))
            if ratio > 1.0:
                findings.append(
                    f"Level {lvl} cleared at {cleared[lvl] / 60:.1f} min "
                    f"(budget {budget_s / 60:.0f} min)"
                )
        else:
            sub = 0.0
            findings.append(f"Level {lvl} was never cleared during the watched session")
        total += fracs[lvl] * sub
    return total, findings


# --------------------------------------------------------------------------
# Wiring
# --------------------------------------------------------------------------

def resolve_python(problem: str, override: str | None) -> Path:
    return Path(override) if override else PREP_ROOT / "problems" / problem / "starter.py"


def resolve_go(problem: str, override: str | None) -> str:
    return override if override else PROBLEM_DIRS[problem]


def cmd_list(_args: argparse.Namespace) -> None:
    for problem, go_pkg in PROBLEM_DIRS.items():
        py_file = resolve_python(problem, None)
        py_levels = discover_python_tests(py_file) if py_file.exists() else {}
        try:
            go_levels = discover_go_tests(go_pkg)
        except Exception:
            go_levels = {}
        print(f"{problem}")
        print(f"  python : levels {sorted(py_levels)} ({py_file})")
        print(f"  go     : levels {sorted(go_levels)} (go/{go_pkg})")


def print_report(problem: str, lang: str, results, corr_breakdown, correctness,
                  quality, quality_findings, time_score, time_findings, details) -> float:
    print(f"\n=== {problem} ({lang}) ===")
    for lvl in sorted(results):
        info = corr_breakdown[lvl]
        print(f"  Level {lvl}: {info['passed']}/{info['of']} tests passed "
              f"(weight {info['weight']*100:.0f}%, contributes {info['contribution']*100:.1f}%)")
        for name, msg in details.get(lvl, []):
            print(f"      FAIL {name}: {msg}")

    print(f"  Correctness: {correctness*100:.1f}%")

    print(f"  Code quality: {quality*100:.1f}%")
    for f in quality_findings:
        print(f"      - {f}")

    print(f"  Time efficiency: {time_score*100:.1f}%")
    for f in time_findings:
        print(f"      - {f}")

    composite = (WEIGHTS["correctness"] * correctness
                 + WEIGHTS["quality"] * quality
                 + WEIGHTS["time"] * time_score)
    final = SCALE_MIN + (SCALE_MAX - SCALE_MIN) * composite
    print(f"  Composite: {WEIGHTS['correctness']}*correctness + {WEIGHTS['quality']}*quality "
          f"+ {WEIGHTS['time']}*time = {composite*100:.1f}%")
    print(f"  Modeled score: {final:.0f} / {SCALE_MAX} (scale starts at {SCALE_MIN})")
    if final >= REPORTED_CUTOFF:
        print(f"  Verdict: would likely CLEAR the reported ~{REPORTED_CUTOFF}/{SCALE_MAX} cutoff")
    else:
        print(f"  Verdict: {REPORTED_CUTOFF - final:.0f} points short of the reported "
              f"~{REPORTED_CUTOFF}/{SCALE_MAX} cutoff")
    return final


def grade_one(problem: str, lang: str, override, timeout: float) -> float | None:
    if lang == "python":
        file_path = resolve_python(problem, override)
        if not file_path.exists():
            print(f"{problem}: {file_path} not found, skipping")
            return None
        levels = discover_python_tests(file_path)
        if not levels:
            print(f"{problem}: no test_level_* functions found, skipping")
            return None
        results, details = run_all_tests(problem, lang, file_path, levels, timeout)
        quality, quality_findings = assess_python_quality(file_path.read_text())
    else:
        pkg_name = resolve_go(problem, override)
        levels = discover_go_tests(pkg_name)
        if not levels:
            print(f"{problem}: no TestLevel* functions found in go/{pkg_name}, skipping")
            return None
        results, details = run_all_tests(problem, lang, pkg_name, levels, timeout)
        quality, quality_findings = assess_go_quality(pkg_name)

    correctness, corr_breakdown = score_correctness(results)
    cleared = load_timing_log(problem, lang)
    time_score, time_findings = score_time(cleared, list(levels))

    return print_report(problem, lang, results, corr_breakdown, correctness,
                         quality, quality_findings, time_score, time_findings, details)


def cmd_score(args: argparse.Namespace) -> None:
    problems = list(PROBLEM_DIRS) if args.all else [args.problem]
    scores = []
    for problem in problems:
        override = args.file if args.lang == "python" else args.dir
        final = grade_one(problem, args.lang, override, args.timeout)
        if final is not None:
            scores.append(final)
    if args.all and scores:
        print(f"\n=== summary ({args.lang}) ===")
        print(f"  average modeled score: {sum(scores)/len(scores):.0f} / {SCALE_MAX} "
              f"across {len(scores)} problems")


def cmd_watch(args: argparse.Namespace) -> None:
    problem, lang, timeout = args.problem, args.lang, args.timeout
    if lang == "python":
        file_path = resolve_python(problem, args.file)
        levels = discover_python_tests(file_path)
    else:
        file_path = resolve_go(problem, args.dir)
        levels = discover_go_tests(file_path)
    if not levels:
        print(f"{problem}: no tests discovered, nothing to watch")
        return

    watched_mtime_path = (PREP_ROOT / "problems" / problem / "starter.py") if lang == "python" \
        else (GO_ROOT / file_path)
    print(f"Watching {problem} ({lang}). Save the file after each change; Ctrl+C when you're done "
          f"implementing (or after clearing the last level) to save the timing log.")

    start = time.monotonic()
    cleared: dict[int, float] = {}
    last_mtime = None
    try:
        while True:
            try:
                mtime = max(p.stat().st_mtime for p in Path(watched_mtime_path).glob("*")) \
                    if Path(watched_mtime_path).is_dir() else Path(watched_mtime_path).stat().st_mtime
            except FileNotFoundError:
                mtime = None
            if mtime != last_mtime:
                last_mtime = mtime
                time.sleep(0.3)  # debounce editor saves
                results, _details = run_all_tests(problem, lang, file_path, levels, timeout)
                for lvl, passes in sorted(results.items()):
                    if lvl not in cleared and passes and all(passes):
                        cleared[lvl] = time.monotonic() - start
                        print(f"  Level {lvl} cleared at {cleared[lvl]/60:.1f} min")
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    log_path = timing_log_path(problem, lang)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(cleared, indent=2))
    print(f"\nSaved timing log to {log_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="show discoverable problems/levels for both languages")
    p_list.set_defaults(func=cmd_list)

    p_score = sub.add_parser("score", help="grade one attempt (or --all attempts) once")
    p_score.add_argument("--lang", choices=["python", "go"], required=True)
    p_score.add_argument("--problem", help="problem name, e.g. key_value_store")
    p_score.add_argument("--all", action="store_true", help="grade every problem for this language")
    p_score.add_argument("--file", help="override the Python file to grade")
    p_score.add_argument("--dir", help="override the Go package dir name to grade")
    p_score.add_argument("--timeout", type=float, default=TEST_TIMEOUT_SECONDS)
    p_score.set_defaults(func=cmd_score)

    p_watch = sub.add_parser("watch", help="live-rerun tests as you edit, to log real level-clearing times")
    p_watch.add_argument("--lang", choices=["python", "go"], required=True)
    p_watch.add_argument("--problem", required=True)
    p_watch.add_argument("--file", help="override the Python file to watch")
    p_watch.add_argument("--dir", help="override the Go package dir name to watch")
    p_watch.add_argument("--timeout", type=float, default=TEST_TIMEOUT_SECONDS)
    p_watch.set_defaults(func=cmd_watch)

    args = parser.parse_args()
    if args.command == "score" and not args.all and not args.problem:
        parser.error("score requires --problem or --all")
    args.func(args)


if __name__ == "__main__":
    main()
