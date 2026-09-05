"""Staged practice timer for CodeSignal-style progressive assessments.

Standard library only, matching the real assessment's constraints. Run it
stand-alone while you work through a problem in `problems/`:

    python3 timer.py
    python3 timer.py --minutes 90 --stages 6
    python3 timer.py --stages "Data model:20,Level 1:15,Level 2:15,Level 3:15,Level 4:15,Buffer:10"

With no arguments it budgets 90 minutes across six default stages, matching
the "assume six stages, not four" guidance in STRATEGY.md.
"""
from __future__ import annotations

import argparse
import sys
import time

DEFAULT_STAGES = [
    ("Data model", 20),
    ("Level 1", 15),
    ("Level 2", 15),
    ("Level 3", 15),
    ("Level 4", 15),
    ("Buffer / stretch level", 10),
]


def parse_stages(spec: str) -> list[tuple[str, int]]:
    stages = []
    for chunk in spec.split(","):
        name, _, minutes = chunk.rpartition(":")
        stages.append((name.strip(), int(minutes.strip())))
    return stages


def even_split(total_minutes: int, stage_count: int) -> list[tuple[str, int]]:
    base = total_minutes // stage_count
    remainder = total_minutes - base * stage_count
    stages = []
    for i in range(stage_count):
        minutes = base + (1 if i < remainder else 0)
        stages.append((f"Stage {i + 1}", minutes))
    return stages


def countdown(label: str, seconds: int) -> None:
    end = time.monotonic() + seconds
    while True:
        remaining = end - time.monotonic()
        if remaining <= 0:
            break
        mins, secs = divmod(int(remaining) + 1, 60)
        sys.stdout.write(f"\r{label}: {mins:02d}:{secs:02d} remaining   ")
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write(f"\r{label}: 00:00 remaining -- time's up          \n")
    sys.stdout.flush()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--minutes", type=int, default=90, help="total session minutes")
    parser.add_argument("--stages", type=str, default=None,
                         help='either an integer count for an even split, or '
                              '"Name:minutes,Name:minutes,..." for explicit stages')
    args = parser.parse_args()

    if args.stages is None:
        stages = DEFAULT_STAGES
    elif args.stages.isdigit():
        stages = even_split(args.minutes, int(args.stages))
    else:
        stages = parse_stages(args.stages)

    total = sum(minutes for _, minutes in stages)
    print(f"Session plan ({total} min total):")
    for name, minutes in stages:
        print(f"  - {name}: {minutes} min")
    input("\nPress Enter to start...")

    for name, minutes in stages:
        print(f"\n=== {name} ({minutes} min) ===")
        try:
            countdown(name, minutes * 60)
        except KeyboardInterrupt:
            print("\nSession interrupted.")
            return
        input(f"{name} done. Press Enter to continue to the next stage...")

    print("\nSession complete. Do the 5-minute postmortem from README.md now.")


if __name__ == "__main__":
    main()
