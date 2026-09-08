// Package once drills sync.Once: lazily initializing a resource exactly
// once, no matter how many goroutines race to be the first to need it.
package once

import "sync"

type Loader struct {
	once  sync.Once
	value string
}

func NewLoader() *Loader {
	panic("not implemented")
}

// Get returns the loaded value, calling load exactly once across all
// concurrent callers -- even if many goroutines call Get before the
// first load finishes, they must all block until that one load completes
// and then all receive its result.
func (l *Loader) Get(load func() string) string {
	panic("not implemented")
}
