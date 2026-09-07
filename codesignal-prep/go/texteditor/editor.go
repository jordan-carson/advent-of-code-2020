// Package texteditor is a starter for the text editor problem.
// See ../../problems/text_editor/README.md for the full spec.
package texteditor

type Editor struct {
	// TODO: design your Level 1 state here
}

func New() *Editor {
	return &Editor{}
}

// --- Level 1 ---

func (e *Editor) Insert(pos int, text string) {
	panic("not implemented")
}

func (e *Editor) Delete(pos, length int) {
	panic("not implemented")
}

func (e *Editor) GetText() string {
	panic("not implemented")
}

// --- Level 2 ---

// Undo reverts the last insert/delete, returns whether there was anything to undo.
func (e *Editor) Undo() bool {
	panic("not implemented")
}

// Redo reapplies the last undone operation; any new edit after an undo
// clears the redo stack.
func (e *Editor) Redo() bool {
	panic("not implemented")
}

// --- Level 4 ---

func (e *Editor) SetCursor(pos int) {
	panic("not implemented")
}

func (e *Editor) TypeAtCursor(text string) {
	panic("not implemented")
}

func (e *Editor) BackspaceAtCursor(length int) {
	panic("not implemented")
}
