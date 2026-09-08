package selectdemo

import (
	"testing"
	"time"
)

func TestFanIn(t *testing.T) {
	a := make(chan int)
	b := make(chan int)
	c := make(chan int)

	go func() {
		defer close(a)
		a <- 1
		a <- 2
	}()
	go func() {
		defer close(b)
		b <- 3
	}()
	go func() {
		defer close(c)
		c <- 4
		c <- 5
	}()

	out := FanIn(a, b, c)
	seen := map[int]bool{}
	deadline := time.After(2 * time.Second)
	for len(seen) < 5 {
		select {
		case n, ok := <-out:
			if !ok {
				t.Fatalf("output channel closed early, only saw %v", seen)
			}
			seen[n] = true
		case <-deadline:
			t.Fatalf("timed out waiting for all 5 values, only saw %v", seen)
		}
	}
	for _, want := range []int{1, 2, 3, 4, 5} {
		if !seen[want] {
			t.Fatalf("FanIn output %v missing value %d", seen, want)
		}
	}

	select {
	case _, ok := <-out:
		if ok {
			t.Fatalf("expected output channel to be closed after all inputs drained")
		}
	case <-time.After(time.Second):
		t.Fatalf("output channel was never closed after all inputs closed")
	}
}

func TestReceiveWithTimeoutSuccess(t *testing.T) {
	ch := make(chan int, 1)
	ch <- 7
	value, ok := ReceiveWithTimeout(ch, 200*time.Millisecond)
	if !ok || value != 7 {
		t.Fatalf("ReceiveWithTimeout(...) = %d, %v; want 7, true", value, ok)
	}
}

func TestReceiveWithTimeoutExpires(t *testing.T) {
	ch := make(chan int) // never sent to
	start := time.Now()
	_, ok := ReceiveWithTimeout(ch, 50*time.Millisecond)
	elapsed := time.Since(start)
	if ok {
		t.Fatalf("ReceiveWithTimeout ok = true; want false (nothing was ever sent)")
	}
	if elapsed > 500*time.Millisecond {
		t.Fatalf("ReceiveWithTimeout took %s; should return promptly after its own timeout", elapsed)
	}
}
