package ctxutil

import (
	"context"
	"errors"
	"testing"
	"time"
)

func TestRunWithTimeoutFastWorkSucceeds(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	got, err := RunWithTimeout(ctx, func() (int, error) {
		return 42, nil
	})
	if err != nil || got != 42 {
		t.Fatalf("RunWithTimeout(fast work) = %d, %v; want 42, nil", got, err)
	}
}

func TestRunWithTimeoutSlowWorkTimesOut(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 20*time.Millisecond)
	defer cancel()

	start := time.Now()
	_, err := RunWithTimeout(ctx, func() (int, error) {
		time.Sleep(500 * time.Millisecond)
		return 1, nil
	})
	elapsed := time.Since(start)

	if !errors.Is(err, context.DeadlineExceeded) {
		t.Fatalf("RunWithTimeout(slow work) err = %v; want context.DeadlineExceeded", err)
	}
	if elapsed > 200*time.Millisecond {
		t.Fatalf("RunWithTimeout took %s; should return as soon as the context times out, "+
			"not wait for slow work to finish", elapsed)
	}
}

func TestCountUntilCancelStopsPromptly(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())

	go func() {
		time.Sleep(50 * time.Millisecond)
		cancel()
	}()

	done := make(chan int, 1)
	start := time.Now()
	go func() { done <- CountUntilCancel(ctx, 5*time.Millisecond) }()

	select {
	case count := <-done:
		elapsed := time.Since(start)
		if elapsed > 200*time.Millisecond {
			t.Fatalf("CountUntilCancel took %s to notice cancellation; should stop within a tick or two", elapsed)
		}
		if count < 3 {
			t.Fatalf("CountUntilCancel returned %d; expected it to have ticked a few times before cancellation", count)
		}
	case <-time.After(time.Second):
		t.Fatalf("CountUntilCancel never returned after ctx was canceled")
	}
}
