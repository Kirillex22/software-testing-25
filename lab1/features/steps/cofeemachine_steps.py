from behave import given, when, then
from impl import CAPUCCINO_MILK_REQUIRED
from impl.cofeemachine import CofeeMachine, NotEnoughMilkException  # предполагаем, что класс в coffeemachine.py


@given("кофемашина включена и готова к работе")
def step_machine_on(context):
    context.machine = CofeeMachine()


@given('в кофемашину добавлено {amount:d} миллилитров молока')
def step_add_milk(context, amount):
    context.machine.add_milk(amount)
    context.initial_milk = amount


@when("пользователь заказывает капучино")
def step_order_cappuccino(context):
    try:
        context.machine.buy_cappuccino()
        context.exception = None
    except Exception as e:
        context.exception = e


@then("должна произойти ошибка из-за нехватки молока")
def step_check_exception(context):
    assert isinstance(context.exception, NotEnoughMilkException), \
        f"Ожидалось исключение NotEnoughMilkException, получено {type(context.exception)}"


@then("количество молока должно остаться равным {expected:d} миллилитрам")
def step_check_milk_remains(context, expected):
    assert context.machine.milk == expected, \
        f"Ожидалось {expected} мл, получено {context.machine.milk} мл"
