import pytest
from app.calculations import BankAccount, InsufficientFunds, add, subtract, multiply, divide


@pytest.fixture
def zero_bank_account():
    print("Creating empty bank account")
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (3,2,5),
    (7,1,8),
    (12,4,16)
])
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1, num2 ) == expected

def test_subtract():
    print("testing subtract function")
    assert subtract(9, 4) == 5

def test_multiply():
    print("testing  multiply function")
    assert multiply(4, 3) == 12

def test_divide():
    print("testing divide function")
    assert divide(20, 5) == 4


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_withdraw(bank_account):
    #bank_account = BankAccount(50) -- if you dont want to use fixtures
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_bank_deposit(bank_account):
    #bank_account = BankAccount(50)
    bank_account.deposit(20)
    assert bank_account.balance == 70

def test_collect__interest(bank_account):
    #bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55


@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200,100,100),
    (50,10,40),
    (1200,200,1000),
])
def test_bank__transactions(zero_bank_account, deposited, withdrew, expected):
    #bank_account = BankAccount(50)
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_insufficient__funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
