package ratelimiter

import "testing"

func TestLevel1(t *testing.T) {
	l := New(2, 10)
	if !l.Allow("c1", 0) {
		t.Fatalf("Allow(c1, 0) = false; want true")
	}
	if !l.Allow("c1", 1) {
		t.Fatalf("Allow(c1, 1) = false; want true")
	}
	if l.Allow("c1", 2) {
		t.Fatalf("Allow(c1, 2) = true; want false (limit exhausted in this window)")
	}
	if !l.Allow("c1", 11) {
		t.Fatalf("Allow(c1, 11) = false; want true (new window)")
	}
}

func TestLevel2(t *testing.T) {
	l := New(2, 10)
	if !l.AllowSliding("c1", 0) {
		t.Fatalf("AllowSliding(c1, 0) = false; want true")
	}
	if !l.AllowSliding("c1", 5) {
		t.Fatalf("AllowSliding(c1, 5) = false; want true")
	}
	if l.AllowSliding("c1", 6) {
		t.Fatalf("AllowSliding(c1, 6) = true; want false")
	}
	if !l.AllowSliding("c1", 11) {
		t.Fatalf("AllowSliding(c1, 11) = false; want true (t=0 request aged out)")
	}
}

func TestLevel3(t *testing.T) {
	l := New(1, 10)
	l.SetLimit("vip", 5, 10)
	for i := 0; i < 5; i++ {
		if !l.Allow("vip", float64(i)) {
			t.Fatalf("Allow(vip, %d) = false; want true", i)
		}
	}
	if l.Allow("vip", 5) {
		t.Fatalf("Allow(vip, 5) = true; want false (custom limit exhausted)")
	}
	if !l.Allow("regular", 0) {
		t.Fatalf("Allow(regular, 0) = false; want true")
	}
	if l.Allow("regular", 1) {
		t.Fatalf("Allow(regular, 1) = true; want false (default limit is 1)")
	}
}
