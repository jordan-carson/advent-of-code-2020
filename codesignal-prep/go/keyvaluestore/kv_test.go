package keyvaluestore

import (
	"reflect"
	"testing"
	"time"
)

func TestLevel1(t *testing.T) {
	s := New()
	if _, ok := s.Get("a"); ok {
		t.Fatalf("expected missing key to return ok=false")
	}
	s.Set("a", "1")
	if v, ok := s.Get("a"); !ok || v != "1" {
		t.Fatalf("Get(a) = %q, %v; want 1, true", v, ok)
	}
	s.Set("a", "2")
	if v, _ := s.Get("a"); v != "2" {
		t.Fatalf("Get(a) after overwrite = %q; want 2", v)
	}
	if !s.Delete("a") {
		t.Fatalf("Delete(a) = false; want true")
	}
	if s.Delete("a") {
		t.Fatalf("Delete(a) second time = true; want false")
	}
	if _, ok := s.Get("a"); ok {
		t.Fatalf("expected deleted key to return ok=false")
	}
}

func TestLevel2(t *testing.T) {
	s := New()
	for _, k := range []string{"apple", "app", "banana", "apricot"} {
		s.Set(k, k)
	}
	got := s.Scan("ap")
	want := []string{"app", "apple", "apricot"}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("Scan(ap) = %v; want %v", got, want)
	}
	got = s.ScanRange("apple", "banana")
	want = []string{"apple", "apricot", "banana"}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("ScanRange(apple, banana) = %v; want %v", got, want)
	}
}

func TestLevel3(t *testing.T) {
	s := New()
	s.SetWithTTL("temp", "v", 50*time.Millisecond)
	if v, ok := s.Get("temp"); !ok || v != "v" {
		t.Fatalf("Get(temp) immediately = %q, %v; want v, true", v, ok)
	}
	time.Sleep(100 * time.Millisecond)
	if _, ok := s.Get("temp"); ok {
		t.Fatalf("expected expired key to return ok=false")
	}
	if got := s.Scan("t"); len(got) != 0 {
		t.Fatalf("Scan(t) after expiry = %v; want empty", got)
	}
}

func TestLevel4(t *testing.T) {
	s := New()
	s.Set("a", "1")
	s.Set("b", "2")
	snap := s.Snapshot()
	s.Set("a", "changed")
	s.Delete("b")
	s.Restore(snap)
	if v, _ := s.Get("a"); v != "1" {
		t.Fatalf("Get(a) after restore = %q; want 1", v)
	}
	if v, _ := s.Get("b"); v != "2" {
		t.Fatalf("Get(b) after restore = %q; want 2", v)
	}
}
