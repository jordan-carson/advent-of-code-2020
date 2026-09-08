package rwmutex

import (
	"fmt"
	"sync"
	"testing"
)

func TestGetSetBasic(t *testing.T) {
	c := NewCache()
	if _, ok := c.Get("x"); ok {
		t.Fatalf("Get on missing key: ok = true; want false")
	}
	c.Set("x", "hello")
	if got, ok := c.Get("x"); !ok || got != "hello" {
		t.Fatalf("Get(x) = %q, %v; want hello, true", got, ok)
	}
}

// Stress test: many concurrent readers and writers on the same key. This
// mainly proves correctness (no lost/corrupted values, and -race stays
// clean) -- proving readers *overlap* in time needs a benchmark, not a
// unit test; see BenchmarkGet below and the package doc comment.
func TestConcurrentReadersAndWriters(t *testing.T) {
	c := NewCache()
	c.Set("key", "initial")

	var wg sync.WaitGroup
	for w := 0; w < 4; w++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			for i := 0; i < 200; i++ {
				c.Set("key", fmt.Sprintf("writer-%d-%d", id, i))
			}
		}(w)
	}
	for r := 0; r < 8; r++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for i := 0; i < 200; i++ {
				if _, ok := c.Get("key"); !ok {
					t.Errorf("Get(key) ok = false during concurrent writes; want true")
					return
				}
			}
		}()
	}
	wg.Wait()

	if _, ok := c.Get("key"); !ok {
		t.Fatalf("Get(key) ok = false after all writers finished; want true")
	}
}

func BenchmarkGet(b *testing.B) {
	c := NewCache()
	c.Set("key", "value")
	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			c.Get("key")
		}
	})
}
