package waitgroup

import (
	"reflect"
	"testing"
)

func TestRunConcurrently(t *testing.T) {
	tasks := []func() int{
		func() int { return 10 },
		func() int { return 20 },
		func() int { return 30 },
	}
	got := RunConcurrently(tasks)
	want := []int{10, 20, 30}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("RunConcurrently(...) = %v; want %v", got, want)
	}
}

func TestRunConcurrentlyAtScale(t *testing.T) {
	n := 500
	tasks := make([]func() int, n)
	want := make([]int, n)
	for i := 0; i < n; i++ {
		i := i
		tasks[i] = func() int { return i * i }
		want[i] = i * i
	}
	got := RunConcurrently(tasks)
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("RunConcurrently at scale did not preserve order or lost results "+
			"(got len=%d, want len=%d) -- check Add is called before go, not inside the goroutine",
			len(got), len(want))
	}
}

func TestRunConcurrentlyEmpty(t *testing.T) {
	got := RunConcurrently(nil)
	if len(got) != 0 {
		t.Fatalf("RunConcurrently(nil) = %v; want empty", got)
	}
}
