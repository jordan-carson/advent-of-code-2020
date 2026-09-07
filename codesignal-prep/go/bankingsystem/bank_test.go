package bankingsystem

import "testing"

func TestLevel1(t *testing.T) {
	b := New()
	if !b.CreateAccount("a") {
		t.Fatalf("CreateAccount(a) = false; want true")
	}
	if b.CreateAccount("a") {
		t.Fatalf("CreateAccount(a) second time = true; want false")
	}
	if bal, ok := b.Deposit("a", 100); !ok || bal != 100 {
		t.Fatalf("Deposit(a, 100) = %v, %v; want 100, true", bal, ok)
	}
	if bal, ok := b.Deposit("a", 50); !ok || bal != 150 {
		t.Fatalf("Deposit(a, 50) = %v, %v; want 150, true", bal, ok)
	}
	if bal, ok := b.GetBalance("a"); !ok || bal != 150 {
		t.Fatalf("GetBalance(a) = %v, %v; want 150, true", bal, ok)
	}
	if _, ok := b.GetBalance("missing"); ok {
		t.Fatalf("GetBalance(missing) ok = true; want false")
	}
}

func TestLevel2(t *testing.T) {
	b := New()
	b.CreateAccount("a")
	b.CreateAccount("b")
	b.Deposit("a", 100)
	if !b.Transfer("a", "b", 40) {
		t.Fatalf("Transfer(a, b, 40) = false; want true")
	}
	if bal, _ := b.GetBalance("a"); bal != 60 {
		t.Fatalf("GetBalance(a) = %v; want 60", bal)
	}
	if bal, _ := b.GetBalance("b"); bal != 40 {
		t.Fatalf("GetBalance(b) = %v; want 40", bal)
	}
	if b.Transfer("a", "b", 1000) {
		t.Fatalf("Transfer(a, b, 1000) = true; want false (insufficient funds)")
	}
	if bal, _ := b.GetBalance("a"); bal != 60 {
		t.Fatalf("GetBalance(a) after failed transfer = %v; want unchanged 60", bal)
	}
}

func TestLevel3(t *testing.T) {
	b := New()
	b.CreateAccount("a")
	b.CreateAccount("b")
	b.Deposit("a", 100)
	b.Transfer("a", "b", 40)
	history := b.GetHistory("a", "")
	if len(history) != 2 || history[0].Type != "deposit" || history[1].Type != "transfer_out" {
		t.Fatalf("GetHistory(a, \"\") = %+v; want [deposit, transfer_out]", history)
	}
	deposits := b.GetHistory("a", "deposit")
	if len(deposits) != 1 || deposits[0] != history[0] {
		t.Fatalf("GetHistory(a, deposit) = %+v; want just the deposit", deposits)
	}
}

func TestLevel4(t *testing.T) {
	b := New()
	b.CreateAccount("a")
	b.Deposit("a", 100)
	newBalance, ok := b.ApplyInterest("a", 0.05, 365)
	if !ok || newBalance <= 100 {
		t.Fatalf("ApplyInterest(a, 0.05, 365) = %v, %v; want > 100, true", newBalance, ok)
	}
}
