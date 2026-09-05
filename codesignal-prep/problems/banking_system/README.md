# Banking system

Implement `BankingSystem` in `starter.py`. Tests financial precision,
state consistency, and transactional integrity.

## Level 1 — accounts and balances
- `create_account(account_id: str) -> bool` — false if it already exists
- `deposit(account_id: str, amount: float) -> float | None` — returns new
  balance, or `None` if the account doesn't exist
- `get_balance(account_id: str) -> float | None`

## Level 2 — transfers
- `transfer(source_id: str, target_id: str, amount: float) -> bool` —
  fails (returns `False`, no state change) if either account is missing or
  source has insufficient funds

## Level 3 — transaction history with filtering
- `get_history(account_id: str, transaction_type: str | None = None) ->
  list[dict]` — chronological (oldest first) list of `{"type": ...,
  "amount": ..., "timestamp": ...}`, optionally filtered by type
  (`"deposit"`, `"transfer_in"`, `"transfer_out"`)

## Level 4 — interest, time-dependent
- `apply_interest(account_id: str, annual_rate: float, days: int) ->
  float | None` — applies simple or compound interest (pick one, document
  your choice) over the given number of days and returns the new balance

## Level 5 (stretch) — account freezing
- `freeze(account_id: str) -> None` / `unfreeze(account_id: str) -> None`
- All mutating operations on a frozen account fail without side effects;
  reads still work.

## Level 6 (stretch) — scheduled/future-dated transfers
- `schedule_transfer(source_id, target_id, amount, execute_at_day: int)`
- `advance_time(days: int) -> list[bool]` — advances the system clock and
  executes any transfers whose `execute_at_day` has been reached, in the
  order they were scheduled, returning each execution's success.
