// Package buildsystem is a starter for the build system problem.
// See ../../problems/build_system/README.md for the full spec.
package buildsystem

type Builder struct {
	// TODO: design your Level 1 state here
}

func New() *Builder {
	return &Builder{}
}

// --- Level 1 ---

func (b *Builder) AddTask(name string, dependencies []string) {
	panic("not implemented")
}

// BuildOrder returns a valid topological order to build target and
// everything it (transitively) depends on, or (nil, false) on a cycle.
func (b *Builder) BuildOrder(target string) ([]string, bool) {
	panic("not implemented")
}

// --- Level 2 ---

// Run calls executor(taskName) for each task in a valid dependency order
// and returns the order it executed in.
func (b *Builder) Run(target string, executor func(string)) []string {
	panic("not implemented")
}

// --- Level 3 ---

// MarkDirty invalidates a task and everything that transitively depends on it.
func (b *Builder) MarkDirty(name string) {
	panic("not implemented")
}
