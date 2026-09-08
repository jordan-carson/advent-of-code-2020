package ownership

import (
	"sync"
	"testing"
)

func TestSharedCounterConcurrent(t *testing.T) {
	c := NewSharedCounter()
	var wg sync.WaitGroup
	for i := 0; i < 200; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			c.Increment(1)
		}()
	}
	wg.Wait()
	if got := c.Value(); got != 200 {
		t.Fatalf("SharedCounter.Value() = %d; want 200 (run `go test -race` too)", got)
	}
}

func TestOwnedCounterConcurrent(t *testing.T) {
	c := NewOwnedCounter()
	var wg sync.WaitGroup
	for i := 0; i < 200; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			c.Increment(1)
		}()
	}
	wg.Wait()
	if got := c.Value(); got != 200 {
		t.Fatalf("OwnedCounter.Value() = %d; want 200", got)
	}
}
