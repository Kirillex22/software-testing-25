# features/environment.py
from behave.parser import parse_feature

def before_all(context):
    # Принудительно устанавливаем язык русского Gherkin
    context.config.language = "ru"
