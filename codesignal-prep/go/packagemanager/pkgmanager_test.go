package packagemanager

import "testing"

func indexOf(s []string, v string) int {
	for i, x := range s {
		if x == v {
			return i
		}
	}
	return -1
}

func countOf(s []string, v string) int {
	n := 0
	for _, x := range s {
		if x == v {
			n++
		}
	}
	return n
}

func TestLevel1Linear(t *testing.T) {
	m := New()
	m.AddPackage("base", "1.0", nil)
	m.AddPackage("mid", "1.0", []string{"base"})
	m.AddPackage("top", "1.0", []string{"mid"})
	order, ok := m.Install("top")
	if !ok {
		t.Fatalf("Install(top) ok = false; want true")
	}
	if !(indexOf(order, "base") < indexOf(order, "mid") && indexOf(order, "mid") < indexOf(order, "top")) {
		t.Fatalf("Install(top) order = %v; want base before mid before top", order)
	}
}

func TestLevel1Cycle(t *testing.T) {
	m := New()
	m.AddPackage("a", "1.0", []string{"b"})
	m.AddPackage("b", "1.0", []string{"a"})
	if _, ok := m.Install("a"); ok {
		t.Fatalf("Install(a) ok = true; want false (cycle)")
	}
}

func TestLevel1Diamond(t *testing.T) {
	m := New()
	m.AddPackage("base", "1.0", nil)
	m.AddPackage("left", "1.0", []string{"base"})
	m.AddPackage("right", "1.0", []string{"base"})
	m.AddPackage("top", "1.0", []string{"left", "right"})
	order, ok := m.Install("top")
	if !ok {
		t.Fatalf("Install(top) ok = false; want true")
	}
	if countOf(order, "base") != 1 {
		t.Fatalf("Install(top) order = %v; want base exactly once", order)
	}
	if indexOf(order, "base") >= indexOf(order, "left") || indexOf(order, "base") >= indexOf(order, "right") {
		t.Fatalf("Install(top) order = %v; want base before left and right", order)
	}
	if indexOf(order, "left") >= indexOf(order, "top") || indexOf(order, "right") >= indexOf(order, "top") {
		t.Fatalf("Install(top) order = %v; want left and right before top", order)
	}
}
