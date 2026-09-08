package channels

import (
	"reflect"
	"testing"
	"time"
)

func collectWithTimeout(t *testing.T, ch <-chan int, timeout time.Duration) []int {
	t.Helper()
	var got []int
	deadline := time.After(timeout)
	for {
		select {
		case n, ok := <-ch:
			if !ok {
				return got
			}
			got = append(got, n)
		case <-deadline:
			t.Fatalf("timed out waiting for the output channel to close -- " +
				"did every stage close its output once its input was drained?")
			return nil
		}
	}
}

func TestDouble(t *testing.T) {
	in := make(chan int)
	go func() {
		defer close(in)
		for _, n := range []int{1, 2, 3} {
			in <- n
		}
	}()
	got := collectWithTimeout(t, Double(in), time.Second)
	want := []int{2, 4, 6}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("Double(...) = %v; want %v", got, want)
	}
}

func TestDoubleChaining(t *testing.T) {
	in := make(chan int)
	go func() {
		defer close(in)
		in <- 1
		in <- 2
	}()
	got := collectWithTimeout(t, Double(Double(in)), time.Second)
	want := []int{4, 8}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("chained Double(Double(...)) = %v; want %v", got, want)
	}
}

func TestDoubleEmptyInput(t *testing.T) {
	in := make(chan int)
	close(in)
	got := collectWithTimeout(t, Double(in), time.Second)
	if len(got) != 0 {
		t.Fatalf("Double(closed empty channel) = %v; want empty", got)
	}
}
