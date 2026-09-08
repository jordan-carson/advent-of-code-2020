package mutex

import (
	"sync"
	"testing"
)

func TestGetSetBasic(t *testing.T) {
	m := NewSafeMap()
	if _, ok := m.Get("x"); ok {
		t.Fatalf("Get on missing key: ok = true; want false")
	}
	if got := m.Increment("x", 5); got != 5 {
		t.Fatalf("Increment(x, 5) = %d; want 5", got)
	}
	if got, ok := m.Get("x"); !ok || got != 5 {
		t.Fatalf("Get(x) = %d, %v; want 5, true", got, ok)
	}
}

// The test that actually matters: hammer the same key from many
// goroutines and check nothing was lost. Run with `go test -race` -- a
// version that reads then writes without holding the lock across both
// steps will both race *and* undercount here.
func TestIncrementIsAtomicUnderConcurrency(t *testing.T) {
	m := NewSafeMap()
	const goroutines = 50
	const perGoroutine = 200

	var wg sync.WaitGroup
	for i := 0; i < goroutines; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for j := 0; j < perGoroutine; j++ {
				m.Increment("shared", 1)
			}
		}()
	}
	wg.Wait()

	want := goroutines * perGoroutine
	if got, ok := m.Get("shared"); !ok || got != want {
		t.Fatalf("Get(shared) = %d, %v; want %d, true (lost updates under concurrency)", got, ok, want)
	}
}

// Compare against rwmutex.BenchmarkGet with `go test -bench=. -run=^$
// -cpu=4` in each package -- same read-only workload, one plain Mutex,
// one RWMutex. That gap is what RWMutex buys you when reads dominate.
func BenchmarkGet(b *testing.B) {
	m := NewSafeMap()
	m.Increment("key", 1)
	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			m.Get("key")
		}
	})
}
