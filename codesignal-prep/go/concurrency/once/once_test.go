package once

import (
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

func TestGetCallsLoadExactlyOnce(t *testing.T) {
	l := NewLoader()
	var calls int32
	const n = 100
	results := make([]string, n)

	var wg sync.WaitGroup
	for i := 0; i < n; i++ {
		wg.Add(1)
		go func(idx int) {
			defer wg.Done()
			results[idx] = l.Get(func() string {
				atomic.AddInt32(&calls, 1)
				time.Sleep(10 * time.Millisecond) // widen the race window
				return "loaded-value"
			})
		}(i)
	}
	wg.Wait()

	if calls != 1 {
		t.Fatalf("load was called %d times across %d concurrent Get calls; want exactly 1", calls, n)
	}
	for i, r := range results {
		if r != "loaded-value" {
			t.Fatalf("results[%d] = %q; want %q", i, r, "loaded-value")
		}
	}
}

func TestGetIgnoresLoadOnSubsequentCalls(t *testing.T) {
	l := NewLoader()
	first := l.Get(func() string { return "first" })
	second := l.Get(func() string { return "second" })
	if first != "first" || second != "first" {
		t.Fatalf("Get() = %q then %q; want %q then %q (second load func must never run)",
			first, second, "first", "first")
	}
}
