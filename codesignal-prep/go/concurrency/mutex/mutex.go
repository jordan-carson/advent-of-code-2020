// Package mutex drills sync.Mutex: a map[string]int made safe for
// concurrent use by making every operation mutually exclusive. See
// ../rwmutex for the version that lets concurrent reads through.
package mutex

import "sync"

type SafeMap struct {
	mu   sync.Mutex
	data map[string]int
}

func NewSafeMap() *SafeMap {
	panic("not implemented")
}

func (m *SafeMap) Get(key string) (int, bool) {
	panic("not implemented")
}

// Increment adds delta to key's current value (starting from 0 if unset)
// and returns the new value. This must be atomic end-to-end: a
// read-then-write built from two separately-locked calls to Get/Set would
// lose updates under concurrent callers incrementing the same key.
func (m *SafeMap) Increment(key string, delta int) int {
	panic("not implemented")
}
