// Package waitgroup is the idiomatic replacement for the manual
// completion-channel pattern in ../goroutines: sync.WaitGroup is built
// for exactly "run N goroutines, wait for all of them."
//
// The classic footgun: call wg.Add(1) before starting the goroutine, not
// inside it -- if the goroutine hasn't been scheduled yet, Wait() can
// return before Add ever runs, and the WaitGroup panics ("negative
// WaitGroup counter") or just under-counts.
package waitgroup

// RunConcurrently runs each task in its own goroutine and returns their
// results in the same order as tasks, using a sync.WaitGroup to know
// when every goroutine has finished.
func RunConcurrently(tasks []func() int) []int {
	panic("not implemented")
}
