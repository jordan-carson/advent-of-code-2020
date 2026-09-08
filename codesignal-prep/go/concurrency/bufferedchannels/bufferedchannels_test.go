package bufferedchannels

import (
	"testing"
	"time"
)

func TestTryPushWhenFull(t *testing.T) {
	q := NewBoundedQueue(2)
	if !q.TryPush(1) || !q.TryPush(2) {
		t.Fatalf("TryPush should succeed while under capacity")
	}
	if q.TryPush(3) {
		t.Fatalf("TryPush should fail once the queue is at capacity")
	}
}

func TestPushBlocksUntilRoom(t *testing.T) {
	q := NewBoundedQueue(1)
	q.Push(1) // fill it to capacity

	done := make(chan struct{})
	go func() {
		q.Push(2) // must block until Pop below makes room
		close(done)
	}()

	select {
	case <-done:
		t.Fatalf("Push on a full queue returned before room was made")
	case <-time.After(100 * time.Millisecond):
		// expected: still blocked
	}

	if got := q.Pop(); got != 1 {
		t.Fatalf("Pop() = %d; want 1 (FIFO order)", got)
	}

	select {
	case <-done:
		// expected: the pending Push(2) unblocked
	case <-time.After(time.Second):
		t.Fatalf("Push did not unblock after Pop made room")
	}

	if got := q.Pop(); got != 2 {
		t.Fatalf("Pop() = %d; want 2", got)
	}
}

func TestPopBlocksUntilAvailable(t *testing.T) {
	q := NewBoundedQueue(1)
	got := make(chan int, 1)
	go func() { got <- q.Pop() }()

	select {
	case <-got:
		t.Fatalf("Pop on an empty queue returned before anything was pushed")
	case <-time.After(100 * time.Millisecond):
		// expected: still blocked
	}

	q.Push(42)

	select {
	case v := <-got:
		if v != 42 {
			t.Fatalf("Pop() = %d; want 42", v)
		}
	case <-time.After(time.Second):
		t.Fatalf("Pop did not unblock after Push")
	}
}
