// Package channels drills the classic Go pipeline-stage contract: a
// stage receives from an input channel, does its work, sends to an
// output channel, and closes that output channel once (and only once)
// its input has been closed and fully drained. Get this contract wrong
// and callers ranging over your output channel either deadlock forever
// or panic on a double-close.
package channels

// Double reads ints from in, doubles them, and sends them on the
// returned channel. It must close the returned channel once in is closed
// and drained, so callers can `for n := range Double(in)`. Stages built
// this way compose: Double(Double(in)) should just work.
func Double(in <-chan int) <-chan int {
	panic("not implemented")
}
