"""Implement BankingSystem level by level. See README.md for the spec."""
from __future__ import annotations


class BankingSystem:
    def __init__(self) -> None:
        pass  # TODO: design your Level 1 state here

    # --- Level 1 ---
    def create_account(self, account_id: str) -> bool:
        raise NotImplementedError

    def deposit(self, account_id: str, amount: float) -> float | None:
        raise NotImplementedError

    def get_balance(self, account_id: str) -> float | None:
        raise NotImplementedError

    # --- Level 2 ---
    def transfer(self, source_id: str, target_id: str, amount: float) -> bool:
        raise NotImplementedError

    # --- Level 3 ---
    def get_history(self, account_id: str, transaction_type: str | None = None) -> list[dict]:
        raise NotImplementedError

    # --- Level 4 ---
    def apply_interest(self, account_id: str, annual_rate: float, days: int) -> float | None:
        raise NotImplementedError

    # --- Level 5 (stretch) ---
    def freeze(self, account_id: str) -> None:
        raise NotImplementedError

    def unfreeze(self, account_id: str) -> None:
        raise NotImplementedError


def test_level_1() -> None:
    bank = BankingSystem()
    assert bank.create_account("a") is True
    assert bank.create_account("a") is False
    assert bank.deposit("a", 100) == 100
    assert bank.deposit("a", 50) == 150
    assert bank.get_balance("a") == 150
    assert bank.get_balance("missing") is None


def test_level_2() -> None:
    bank = BankingSystem()
    bank.create_account("a")
    bank.create_account("b")
    bank.deposit("a", 100)
    assert bank.transfer("a", "b", 40) is True
    assert bank.get_balance("a") == 60
    assert bank.get_balance("b") == 40
    assert bank.transfer("a", "b", 1000) is False
    assert bank.get_balance("a") == 60


def test_level_3() -> None:
    bank = BankingSystem()
    bank.create_account("a")
    bank.create_account("b")
    bank.deposit("a", 100)
    bank.transfer("a", "b", 40)
    history = bank.get_history("a")
    assert [h["type"] for h in history] == ["deposit", "transfer_out"]
    assert bank.get_history("a", "deposit") == [history[0]]


def test_level_4() -> None:
    bank = BankingSystem()
    bank.create_account("a")
    bank.deposit("a", 100)
    new_balance = bank.apply_interest("a", annual_rate=0.05, days=365)
    assert new_balance is not None and new_balance > 100


if __name__ == "__main__":
    test_level_1()
    print("Level 1 OK")
    test_level_2()
    print("Level 2 OK")
    test_level_3()
    print("Level 3 OK")
    test_level_4()
    print("Level 4 OK")
