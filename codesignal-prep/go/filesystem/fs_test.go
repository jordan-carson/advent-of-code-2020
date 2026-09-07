package filesystem

import "testing"

func TestLevel1(t *testing.T) {
	fs := New()
	if !fs.Mkdir("/a/b") {
		t.Fatalf("Mkdir(/a/b) = false; want true")
	}
	if !fs.WriteFile("/a/b/file.txt", "hello") {
		t.Fatalf("WriteFile(/a/b/file.txt) = false; want true")
	}
	if content, ok := fs.ReadFile("/a/b/file.txt"); !ok || content != "hello" {
		t.Fatalf("ReadFile(/a/b/file.txt) = %q, %v; want hello, true", content, ok)
	}
	if children, ok := fs.ListDir("/a/b"); !ok || len(children) != 1 || children[0] != "file.txt" {
		t.Fatalf("ListDir(/a/b) = %v, %v; want [file.txt], true", children, ok)
	}
	if fs.WriteFile("/missing/file.txt", "x") {
		t.Fatalf("WriteFile with missing parent = true; want false")
	}
	if _, ok := fs.ReadFile("/nope"); ok {
		t.Fatalf("ReadFile(/nope) ok = true; want false")
	}
}

func TestLevel2(t *testing.T) {
	fs := New()
	fs.Mkdir("/a")
	fs.SetPermissions("/a", "alice", "rw")
	fs.WriteFile("/a/f.txt", "content", "alice")
	if fs.WriteFile("/a/f.txt", "nope", "bob") {
		t.Fatalf("WriteFile as non-owner bob = true; want false")
	}
	if content, _ := fs.ReadFile("/a/f.txt", "bob"); content != "content" {
		t.Fatalf("ReadFile as bob = %q; want content (reads allowed for non-owners)", content)
	}
}

func TestLevel3(t *testing.T) {
	fs := New()
	fs.Mkdir("/a")
	fs.WriteFile("/a/real.txt", "hi")
	if !fs.CreateSymlink("/link", "/a/real.txt") {
		t.Fatalf("CreateSymlink(/link, /a/real.txt) = false; want true")
	}
	if content, _ := fs.ReadFile("/link"); content != "hi" {
		t.Fatalf("ReadFile(/link) = %q; want hi", content)
	}
	fs.CreateSymlink("/x", "/y")
	if fs.CreateSymlink("/y", "/x") {
		t.Fatalf("CreateSymlink that would form a cycle = true; want false")
	}
}
