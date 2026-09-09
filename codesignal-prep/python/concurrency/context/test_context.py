"""Run with: python3 test_context.py"""
from __future__ import annotations

import threading
import time

from context import CancelContext, count_until_cancel, run_with_timeout


def test_run_with_timeout_fast_work_succeeds() -> None:
    ctx = CancelContext(timeout=1.0)
    result, err = run_with_timeout(ctx, lambda: 42)
    assert err is None and result == 42, f"run_with_timeout(fast work) = {result}, {err}; want 42, None"


def test_run_with_timeout_slow_work_times_out() -> None:
    ctx = CancelContext(timeout=0.02)

    def slow_work() -> int:
        time.sleep(0.5)
        return 1

    start = time.monotonic()
    _, err = run_with_timeout(ctx, slow_work)
    elapsed = time.monotonic() - start

    assert err is not None, "expected a cancellation/timeout error, got None"
    assert elapsed < 0.2, (
        f"run_with_timeout took {elapsed:.2f}s; should return as soon as ctx "
        "times out, not wait for slow work to finish"
    )


def test_count_until_cancel_stops_promptly() -> None:
    ctx = CancelContext()
    threading.Timer(0.05, ctx.cancel).start()

    result: dict = {}

    def runner() -> None:
        result["count"] = count_until_cancel(ctx, tick=0.005)

    start = time.monotonic()
    t = threading.Thread(target=runner)
    t.start()
    t.join(timeout=1.0)
    elapsed = time.monotonic() - start

    assert not t.is_alive(), "count_until_cancel never returned after ctx was cancelled"
    assert elapsed < 0.3, f"count_until_cancel took {elapsed:.2f}s to notice cancellation"
    count = result.get("count")
    assert count is not None and count >= 3, (
        f"count = {count}; expected several ticks to have happened before cancellation at ~0.05s"
    )


if __name__ == "__main__":
    test_run_with_timeout_fast_work_succeeds()
    print("test_run_with_timeout_fast_work_succeeds OK")
    test_run_with_timeout_slow_work_times_out()
    print("test_run_with_timeout_slow_work_times_out OK")
    test_count_until_cancel_stops_promptly()
    print("test_count_until_cancel_stops_promptly OK")
