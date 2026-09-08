// Package ctxutil (directory "context" -- named to avoid confusion with
// the stdlib "context" package it imports) drills the two canonical uses
// of context.Context: racing work against cancellation, and a
// cooperative loop that checks for cancellation instead of running
// forever.
package ctxutil

import (
	"context"
	"time"
)

// RunWithTimeout runs work in its own goroutine and returns its result,
// unless ctx is canceled or times out first -- in which case it returns
// (0, ctx.Err()) immediately, without waiting for work to finish.
func RunWithTimeout(ctx context.Context, work func() (int, error)) (int, error) {
	panic("not implemented")
}

// CountUntilCancel increments a counter once per tick until ctx is
// canceled, then returns the final count. It must notice cancellation
// promptly (within about one tick), not run to some fixed limit.
func CountUntilCancel(ctx context.Context, tick time.Duration) int {
	panic("not implemented")
}
