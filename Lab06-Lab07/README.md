# L6_L7_18_atm_withdrawal — ATM Withdrawal

Lab 6: Code and Branch Coverage

## About

A small Python module that processes ATM withdrawals with daily limits and fees, checks PIN attempts and works out the note breakup.

## Files

| File | Description |
|------|-------------|
| `atm_withdrawal.py` | The module under test |
| `test_atm_withdrawal.py` | Pytest test suite for the module |
| `coverage_report.txt` | Terminal output of the coverage run |
| `coverage_report.png` | Screenshot of the HTML coverage report |

Refer to the lab handout for instructions.

## Running the tests

```bash
pip install pytest pytest-cov
cd "Lab 6"
pytest test_atm_withdrawal.py --cov=atm_withdrawal --cov-branch --cov-report=term-missing
```

## Coverage

40 tests pass, with 100% statement coverage (34/34) and 100% branch coverage (22/22).
