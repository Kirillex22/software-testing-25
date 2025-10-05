from behave import given, when, then
from impl.auth import Authentificator, TooManyAuthTriesException
from impl import AUTH_TRY_LIMIT


@given('зарегистрирован пользователь "{username}" с паролем "{password}"')
def step_register_user(context, username, password):
    context.auth = Authentificator()
    context.auth.register(username, password)
    context.username = username
    context.password = password


@when('пользователь "{username}" вводит неправильный пароль "{wrong_password}"')
@when('пользователь "{username}" снова вводит неправильный пароль "{wrong_password}"')
def step_wrong_password(context, username, wrong_password):
    try:
        context.result = context.auth.authenticate(username, wrong_password)
        context.exception = None
    except Exception as e:
        context.exception = e


@then("должна произойти ошибка блокировки аккаунта")
def step_too_many_tries(context):
    assert isinstance(context.exception, TooManyAuthTriesException), \
        f"Ожидалось исключение TooManyAuthTriesException, получено {type(context.exception)}"

