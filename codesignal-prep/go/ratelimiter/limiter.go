// Package ratelimiter is a starter for the rate limiter problem.
// See ../../problems/rate_limiter/README.md for the full spec.
//
// All time values are passed in explicitly as `now` (seconds, as a
// float64) -- don't call time.Now() yourself, so tests stay deterministic.
package ratelimiter

type Limiter struct {
	Limit      int
	WindowSecs float64
	// TODO: design your Level 1 per-client state here
}

func New(limit int, windowSecs float64) *Limiter {
	return &Limiter{Limit: limit, WindowSecs: windowSecs}
}

// --- Level 1 ---

func (l *Limiter) Allow(clientID string, now float64) bool {
	panic("not implemented")
}

// --- Level 2 ---

func (l *Limiter) AllowSliding(clientID string, now float64) bool {
	panic("not implemented")
}

// --- Level 3 ---

func (l *Limiter) SetLimit(clientID string, limit int, windowSecs float64) {
	panic("not implemented")
}

// --- Level 4 ---

func (l *Limiter) AllowBucket(clientID string, now float64, cost int) bool {
	panic("not implemented")
}
