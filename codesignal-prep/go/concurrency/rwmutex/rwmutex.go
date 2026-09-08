// Package rwmutex drills sync.RWMutex: many goroutines can hold the read
// lock at once, but a write excludes everyone (readers and other
// writers). Once this passes, try benchmarking it against ../mutex with
// an equivalent read-heavy workload (`go test -bench=. -run=^$ -cpu=4`
// in each package) to see the actual throughput difference RWMutex buys
// you when reads dominate writes.
package rwmutex

import "sync"

type Cache struct {
	mu   sync.RWMutex
	data map[string]string
}

func NewCache() *Cache {
	panic("not implemented")
}

// Get should use RLock, not Lock -- that's the entire point of this type.
func (c *Cache) Get(key string) (string, bool) {
	panic("not implemented")
}

func (c *Cache) Set(key, value string) {
	panic("not implemented")
}
