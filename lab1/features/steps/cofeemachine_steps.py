from behave import given, when, then
from impl import CAPUCCINO_MILK_REQUIRED
from impl.cofeemachine import CofeeMachine, NotEnoughMilkException


@given("кофемашина включена и готова к работе")
def step_machine_on(context):
    context.machine = CofeeMachine()


@when("пользователь пытается приготовить капучино при разных объёмах молока:")
def step_prepare_multiple(context):
    context.results = []

    for row in context.table:
        milk = int(row["milk"])
        expect_error = row["expect_error"].lower() == "true"

        # каждая попытка — своя "машина", чтобы не смешивать состояние
        machine = CofeeMachine()
        machine.add_milk(milk)

        try:
            machine.buy_cappuccino()
            exception = None
        except Exception as e:
            exception = e

        context.results.append({
            "milk": milk,
            "expect_error": expect_error,
            "exception": exception,
            "remain": machine.milk
        })


@then("результаты приготовления должны соответствовать ожиданиям")
def step_check_results(context):
    for result in context.results:
        milk = result["milk"]
        expect_error = result["expect_error"]
        exception = result["exception"]
        remain = result["remain"]

        if expect_error:
            assert isinstance(exception, NotEnoughMilkException), (
                f"При {milk} мл ожидалась ошибка NotEnoughMilkException, но получено {type(exception)}"
            )
            assert remain == milk, (
                f"При {milk} мл ожидалось, что молоко останется {milk} мл, получено {remain} мл"
            )
        else:
            assert exception is None, f"При {milk} мл не ожидалось ошибок, но получено {exception}"
            assert remain == milk - CAPUCCINO_MILK_REQUIRED, (
                f"При {milk} мл ожидалось, что останется {milk - CAPUCCINO_MILK_REQUIRED}, получено {remain}"
            )
