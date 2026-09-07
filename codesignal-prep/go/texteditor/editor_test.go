package texteditor

import (
	"fmt"
	"testing"
	"time"
)

func TestLevel1(t *testing.T) {
	e := New()
	e.Insert(0, "hello")
	if got := e.GetText(); got != "hello" {
		t.Fatalf("GetText() = %q; want hello", got)
	}
	e.Insert(5, " world")
	if got := e.GetText(); got != "hello world" {
		t.Fatalf("GetText() = %q; want %q", got, "hello world")
	}
	e.Delete(5, 6)
	if got := e.GetText(); got != "hello" {
		t.Fatalf("GetText() = %q; want hello", got)
	}
}

func TestLevel2(t *testing.T) {
	e := New()
	e.Insert(0, "hello")
	e.Insert(5, " world")
	if !e.Undo() {
		t.Fatalf("Undo() = false; want true")
	}
	if got := e.GetText(); got != "hello" {
		t.Fatalf("GetText() after undo = %q; want hello", got)
	}
	if !e.Redo() {
		t.Fatalf("Redo() = false; want true")
	}
	if got := e.GetText(); got != "hello world" {
		t.Fatalf("GetText() after redo = %q; want %q", got, "hello world")
	}
	e.Insert(11, "!")
	if e.Redo() {
		t.Fatalf("Redo() after a new edit = true; want false (redo stack cleared)")
	}
}

func TestLevel3Perf(t *testing.T) {
	e := New()
	start := time.Now()
	for i := 0; i < 3000; i++ {
		e.Insert(i, "x")
	}
	elapsed := time.Since(start)
	fmt.Printf("3000 inserts took %s -- should stay well under a second\n", elapsed)
}
