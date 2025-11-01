from behave import given, when, then
from impl.atm import ATM, NotEnoughMoneyException

@given("в банкомате зарегистрированы пользователи:")
def step_add_accounts(context):
    context.atm = ATM()
    context.users = [row.as_dict() for row in context.table]
    for user in context.users:
        name = user["name"]
        balance = int(user["balance"])
        context.atm.add_account(name)
        context.atm.deposit(name, balance)


@when("пользователи пытаются снять деньги")
def step_withdraw(context):
    for user in context.users:
        name = user["name"]
        withdraw = int(user["withdraw"])
        try:
            context.atm.withdraw(name, withdraw)
            user["error"] = None
        except Exception as e:
            user["error"] = e


@then("результаты операций должны соответствовать ожиданиям")
def step_check_results(context):
    for user in context.users:
        name = user["name"]
        expected_balance = int(user["expected_balance"])
        expect_error = user["expect_error"].lower() == "true"
        balance = context.atm.get_balance(name)

        if expect_error:
            assert isinstance(user["error"], NotEnoughMoneyException), \
                f"Для {name} ожидалась ошибка NotEnoughMoneyException, но получено {user['error']}"
        else:
            assert user["error"] is None, \
                f"Для {name} не ожидалось ошибок, но получено {user['error']}"

        assert balance == expected_balance, \
            f"Баланс {name}: ожидалось {expected_balance}, получено {balance}"