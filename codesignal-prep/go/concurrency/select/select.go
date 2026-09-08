// Package selectdemo (directory "select" -- "select" itself is a
// reserved keyword, so the package identifier can't be that) drills the
// two things select is for: merging multiple channels (fan-in) and
// racing a channel receive against a timeout.
package selectdemo

import "time"

// FanIn merges values from multiple input channels into one output
// channel, in whatever order they actually arrive. Close the output
// channel once every input channel has been closed and drained.
func FanIn(inputs ...<-chan int) <-chan int {
	panic("not implemented")
}

// ReceiveWithTimeout returns the next value sent on ch, or ok=false if
// nothing arrives within timeout.
func ReceiveWithTimeout(ch <-chan int, timeout time.Duration) (value int, ok bool) {
	panic("not implemented")
}
