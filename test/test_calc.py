import pytest
from app.calculations import add, fpow, BankAccount, LackMoney

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    wynik = add(num1, num2)
    assert wynik == expected

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_deposit(zero_bank_account):
    zero_bank_account.deposit(30)
    assert zero_bank_account.balance == 30

def test_bank_withdraw(bank_account):
    bank_account.withdraw(10)
    assert bank_account.balance == 40

def test_bank_collect_intrest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

@pytest.mark.parametrize("deposit, withdrew, expected", [
    (200, 100, 100),
    (50, 40, 10),
    (600, 550, 50)
])
def test_bank_transaction(zero_bank_account, deposit, withdrew, expected):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_lack_of_money(bank_account):

    with pytest.raises(LackMoney):
        bank_account.withdraw(200)

