// Package bufferedchannels drills the one idea buffered channels give
// you for free: a fixed-capacity, concurrency-safe FIFO queue with
// blocking-when-full and blocking-when-empty built in. The buffer
// capacity *is* the bound.
package bufferedchannels

// BoundedQueue is a fixed-capacity FIFO queue built directly on a
// buffered channel.
type BoundedQueue struct {
	items chan int
}

func NewBoundedQueue(capacity int) *BoundedQueue {
	panic("not implemented")
}

// Push blocks until there is room in the queue.
func (q *BoundedQueue) Push(item int) {
	panic("not implemented")
}

// TryPush returns false immediately if the queue is at capacity, instead
// of blocking. (Hint: select with a default case.)
func (q *BoundedQueue) TryPush(item int) bool {
	panic("not implemented")
}

// Pop blocks until an item is available.
func (q *BoundedQueue) Pop() int {
	panic("not implemented")
}
