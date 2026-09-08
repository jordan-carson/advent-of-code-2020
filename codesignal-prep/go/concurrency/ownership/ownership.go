// Package ownership drills Go's core concurrency philosophy: "Don't
// communicate by sharing memory; share memory by communicating."
//
// You'll implement the same counter twice:
//   - SharedCounter: a mutex guards state that any goroutine can touch.
//   - OwnedCounter: a single goroutine owns the state; every other
//     goroutine talks to it by sending messages over a channel. No field
//     is ever read or written from more than one goroutine, so there is
//     nothing to lock.
//
// Both must behave identically from the outside. The point isn't that one
// is "better" -- it's building the instinct to reach for message passing
// (an owner goroutine + a request channel) as a first-class alternative
// to a mutex, not just a mutex with extra steps.
package ownership

import "sync"

// --- Shared-memory style ---

type SharedCounter struct {
	mu    sync.Mutex
	value int
}

func NewSharedCounter() *SharedCounter {
	return &SharedCounter{}
}

func (c *SharedCounter) Increment(delta int) {
	panic("not implemented")
}

func (c *SharedCounter) Value() int {
	panic("not implemented")
}

// --- Message-passing style ---

// command is a message sent to the owning goroutine. If reply is non-nil
// the owner must send the resulting value back on it exactly once.
type command struct {
	delta int
	reply chan int
}

type OwnedCounter struct {
	commands chan command
}

// NewOwnedCounter starts the owning goroutine and returns a handle to it.
// The owning goroutine should loop forever (until the caller stops
// sending, which these tests never do -- a leaked goroutine per test is
// fine here), and be the *only* code that ever touches the counter value.
func NewOwnedCounter() *OwnedCounter {
	panic("not implemented")
}

func (c *OwnedCounter) Increment(delta int) {
	panic("not implemented")
}

func (c *OwnedCounter) Value() int {
	panic("not implemented")
}
