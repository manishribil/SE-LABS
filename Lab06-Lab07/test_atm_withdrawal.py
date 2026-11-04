import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup


# Example test cases:
def test_simple_withdrawal():
    assert withdraw(5000, 1000, "savings", True) == 4000


def test_correct_pin():
    assert pin_check(1234, 1234, 0) == "ok"


# ---------- withdraw: input validation ----------

def test_withdraw_unknown_account_raises():
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(5000, 1000, "salary", True)


@pytest.mark.parametrize("amount", [0, -100, 150])
def test_withdraw_invalid_amount_raises(amount):
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, amount, "savings", True)


def test_withdraw_unknown_account_is_checked_before_amount():
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(5000, 150, "salary", True)


# ---------- withdraw: daily limit ----------

@pytest.mark.parametrize(
    "account_type, amount, expected",
    [
        ("savings", 25000, 75000),          # exactly on the limit
        ("savings", 25100, "limit exceeded"),
        ("current", 50000, 50000),          # exactly on the limit
        ("current", 50100, "limit exceeded"),
    ],
)
def test_withdraw_daily_limit(account_type, amount, expected):
    assert withdraw(100000, amount, account_type, True) == expected


def test_withdraw_limit_is_checked_before_balance():
    assert withdraw(100, 25100, "savings", True) == "limit exceeded"


# ---------- withdraw: fees for other-bank ATMs ----------

def test_own_bank_pays_no_fee():
    assert withdraw(20000, 15000, "savings", True) == 5000


def test_other_bank_small_amount_pays_base_fee():
    assert withdraw(5000, 1000, "savings", False) == 3980


def test_other_bank_fee_at_10000_has_no_surcharge():
    assert withdraw(20000, 10000, "savings", False) == 9980


def test_other_bank_fee_above_10000_has_surcharge():
    assert withdraw(20000, 10100, "savings", False) == 9870


# ---------- withdraw: balance ----------

def test_own_bank_amount_above_balance_is_insufficient():
    assert withdraw(900, 1000, "savings", True) == "insufficient funds"


def test_own_bank_can_withdraw_entire_balance():
    assert withdraw(1000, 1000, "savings", True) == 0


def test_other_bank_fee_pushes_total_above_balance():
    assert withdraw(1000, 1000, "savings", False) == "insufficient funds"


def test_other_bank_balance_exactly_covers_amount_and_fee():
    assert withdraw(1020, 1000, "savings", False) == 0


def test_other_bank_surcharge_pushes_total_above_balance():
    assert withdraw(10120, 10100, "current", False) == "insufficient funds"


def test_other_bank_balance_exactly_covers_amount_and_surcharge():
    assert withdraw(10130, 10100, "current", False) == 0


# ---------- pin_check ----------

@pytest.mark.parametrize("attempts", [3, 4])
def test_pin_blocked_once_attempts_used_up(attempts):
    assert pin_check(1234, 1234, attempts) == "card blocked"


def test_correct_pin_on_last_attempt():
    assert pin_check(1234, 1234, 2) == "ok"


def test_wrong_pin_on_last_attempt_blocks_card():
    assert pin_check(1111, 1234, 2) == "card blocked"


@pytest.mark.parametrize("attempts", [0, 1])
def test_wrong_pin_with_attempts_left_retries(attempts):
    assert pin_check(1111, 1234, attempts) == "retry"


# ---------- note_breakup ----------

@pytest.mark.parametrize("amount", [50, 150, 1099])
def test_note_breakup_invalid_amount_raises(amount):
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(amount)


@pytest.mark.parametrize(
    "amount, expected",
    [
        (0, (0, 0, 0)),
        (100, (0, 0, 1)),      # remainder below 200
        (200, (0, 1, 0)),      # remainder exactly 200
        (300, (0, 1, 1)),      # one 200 and one 100
        (400, (0, 2, 0)),      # two 200s
        (500, (1, 0, 0)),      # exact 500
        (600, (1, 0, 1)),      # 500 and a 100
        (900, (1, 2, 0)),      # 500 and two 200s
        (2800, (5, 1, 1)),     # all three notes
    ],
)
def test_note_breakup(amount, expected):
    assert note_breakup(amount) == expected
