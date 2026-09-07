// Package filesystem is a starter for the file system simulator problem.
// See ../../problems/file_system/README.md for the full spec.
package filesystem

type FS struct {
	// TODO: design your Level 1 state here (think tree vs. flat path map)
}

func New() *FS {
	return &FS{}
}

// --- Level 1 ---

// Mkdir creates all missing intermediate directories (like mkdir -p).
// Returns false if path already exists as a file.
func (fs *FS) Mkdir(path string) bool {
	panic("not implemented")
}

// WriteFile requires the parent directory to already exist. asUser is
// variadic so Level 1 callers (no user context) keep compiling once Level 2
// adds permission checks -- Go has no default arguments, so this is the
// idiomatic way to extend a signature without rewriting every call site.
// Treat a missing asUser as "no permission check" (Level 1 behavior).
func (fs *FS) WriteFile(path, content string, asUser ...string) bool {
	panic("not implemented")
}

func (fs *FS) ReadFile(path string, asUser ...string) (string, bool) {
	panic("not implemented")
}

// ListDir returns sorted immediate children, or (nil, false) if path doesn't exist.
func (fs *FS) ListDir(path string) ([]string, bool) {
	panic("not implemented")
}

// --- Level 2 ---

func (fs *FS) SetPermissions(path, owner, mode string) bool {
	panic("not implemented")
}

// --- Level 3 ---

func (fs *FS) CreateSymlink(path, target string) bool {
	panic("not implemented")
}

// --- Level 4 ---

func (fs *FS) Mount(path string, other *FS) bool {
	panic("not implemented")
}
