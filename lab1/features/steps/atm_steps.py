from behave import given, when, then
from impl.atm import ATM, NotEnoughMoneyException  # предполагаем, что класс ATM в файле atm.py
import pytest

@given('в банкомате зарегистрирован счёт пользователя "{name}"')
def step_add_account(context, name):
    context.atm = ATM()
    context.atm.add_account(name)
    context.account_name = name

@given('на счёт "{name}" зачислено {amount:d} рублей')
def step_deposit(context, name, amount):
    context.atm.deposit(name, amount)

@when('пользователь "{name}" пытается снять {amount:d} рублей')
def step_withdraw(context, name, amount):
    try:
        context.atm.withdraw(name, amount)
        context.withdraw_exception = None
    except Exception as e:
        context.withdraw_exception = e

@then('операция должна быть отклонена')
def step_check_exception(context):
    assert isinstance(context.withdraw_exception, NotEnoughMoneyException), \
        f"Ожидалось исключение NotEnoughMoneyException, получено: {type(context.withdraw_exception)}"

@then('баланс счёта "{name}" должен остаться равным {expected:d} рублей')
def step_check_balance(context, name, expected):
    balance = context.atm.get_balance(name)
    assert balance == expected, f"Ожидалось {expected}, получено {balance}"
