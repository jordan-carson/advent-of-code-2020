// Package goroutines is the warm-up: fan out one goroutine per unit of
// work, and know when all of them are done -- without sync.WaitGroup yet
// (that's the next package; you'll feel exactly what it replaces).
package goroutines

// Squares computes the square of each number concurrently -- one
// goroutine per element -- and returns results in the same order as the
// input. Each goroutine should write only to its own index of the result
// slice (distinct indices are safe to write concurrently, no lock
// needed), and the function must not return until every goroutine has
// finished. Use a plain channel as the completion signal.
func Squares(nums []int) []int {
	panic("not implemented")
}
