package buildsystem

import "testing"

func indexOf(s []string, v string) int {
	for i, x := range s {
		if x == v {
			return i
		}
	}
	return -1
}

func TestLevel1(t *testing.T) {
	b := New()
	b.AddTask("compile", []string{"fetch_deps"})
	b.AddTask("fetch_deps", nil)
	b.AddTask("test", []string{"compile"})
	order, ok := b.BuildOrder("test")
	if !ok {
		t.Fatalf("BuildOrder(test) ok = false; want true")
	}
	if !(indexOf(order, "fetch_deps") < indexOf(order, "compile") && indexOf(order, "compile") < indexOf(order, "test")) {
		t.Fatalf("BuildOrder(test) = %v; want fetch_deps before compile before test", order)
	}

	b2 := New()
	b2.AddTask("a", []string{"b"})
	b2.AddTask("b", []string{"a"})
	if _, ok := b2.BuildOrder("a"); ok {
		t.Fatalf("BuildOrder(a) ok = true; want false (cycle)")
	}
}

func TestLevel2(t *testing.T) {
	b := New()
	b.AddTask("compile", []string{"fetch_deps"})
	b.AddTask("fetch_deps", nil)
	var executed []string
	order := b.Run("compile", func(name string) { executed = append(executed, name) })
	want := []string{"fetch_deps", "compile"}
	if len(executed) != 2 || executed[0] != want[0] || executed[1] != want[1] {
		t.Fatalf("executed = %v; want %v", executed, want)
	}
	if len(order) != 2 || order[0] != want[0] || order[1] != want[1] {
		t.Fatalf("Run order = %v; want %v", order, want)
	}
}

func TestLevel3(t *testing.T) {
	b := New()
	b.AddTask("compile", []string{"fetch_deps"})
	b.AddTask("fetch_deps", nil)
	b.AddTask("test", []string{"compile"})

	var executed []string
	record := func(name string) { executed = append(executed, name) }

	b.Run("test", record)
	want := []string{"fetch_deps", "compile", "test"}
	if len(executed) != 3 {
		t.Fatalf("first Run executed = %v; want %v", executed, want)
	}

	executed = nil
	b.Run("test", record)
	if len(executed) != 0 {
		t.Fatalf("second Run (nothing dirty) executed = %v; want none", executed)
	}

	b.MarkDirty("fetch_deps")
	executed = nil
	b.Run("test", record)
	if len(executed) != 3 {
		t.Fatalf("Run after MarkDirty(fetch_deps) executed = %v; want the whole downstream chain", executed)
	}
}
