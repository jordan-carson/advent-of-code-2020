// Package bankingsystem is a starter for the banking system problem.
// See ../../problems/banking_system/README.md for the full spec.
package bankingsystem

type Transaction struct {
	Type      string // "deposit", "transfer_in", "transfer_out"
	Amount    float64
	Timestamp int64
}

type Bank struct {
	// TODO: design your Level 1 state here
}

func New() *Bank {
	return &Bank{}
}

// --- Level 1 ---

func (b *Bank) CreateAccount(accountID string) bool {
	panic("not implemented")
}

// Deposit returns the new balance and true, or (0, false) if the account doesn't exist.
func (b *Bank) Deposit(accountID string, amount float64) (float64, bool) {
	panic("not implemented")
}

func (b *Bank) GetBalance(accountID string) (float64, bool) {
	panic("not implemented")
}

// --- Level 2 ---

func (b *Bank) Transfer(sourceID, targetID string, amount float64) bool {
	panic("not implemented")
}

// --- Level 3 ---

// GetHistory returns transactions in chronological order (oldest first).
// If transactionType is "", all types are included.
func (b *Bank) GetHistory(accountID, transactionType string) []Transaction {
	panic("not implemented")
}

// --- Level 4 ---

func (b *Bank) ApplyInterest(accountID string, annualRate float64, days int) (float64, bool) {
	panic("not implemented")
}

// --- Level 5 (stretch) ---

func (b *Bank) Freeze(accountID string)   { panic("not implemented") }
func (b *Bank) Unfreeze(accountID string) { panic("not implemented") }
