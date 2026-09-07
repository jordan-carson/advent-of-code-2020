// Package packagemanager is a starter for the package manager problem.
// See ../../problems/package_manager/README.md for the full spec.
package packagemanager

type Manager struct {
	// TODO: design your Level 1 state here (think graph representation)
}

func New() *Manager {
	return &Manager{}
}

// --- Level 1 ---

func (m *Manager) AddPackage(name, version string, dependencies []string) {
	panic("not implemented")
}

// Install returns a topologically sorted install order (dependencies
// before dependents), or (nil, false) if a dependency cycle exists.
func (m *Manager) Install(name string) ([]string, bool) {
	panic("not implemented")
}
