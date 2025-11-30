import pandas as pd
import great_expectations as gx
import os

from great_expectations.data_context import BaseDataContext
from great_expectations.core.batch import BatchRequest
from great_expectations.checkpoint import SimpleCheckpoint


# ============================================================
# 1. ИНИЦИАЛИЗАЦИЯ КОНТЕКСТА GE
# ============================================================

# Создаем необходимые директории
os.makedirs("gx/expectations", exist_ok=True)
os.makedirs("gx/validations", exist_ok=True)
os.makedirs("gx/uncommitted/data_docs", exist_ok=True)

# В версии 0.18.21 проще использовать встроенные методы для создания контекста
context = gx.get_context(mode="file")

# ============================================================
# 2. ДОБАВЛЕНИЕ ИСТОЧНИКОВ ДАННЫХ
# ============================================================

# CSV datasource
pandas_ds = context.sources.add_pandas(
    name="pandas_ref"
)

# SQLite datasource
sqlite_ds = context.sources.add_sqlite(
    name="sqlite_prod",
    connection_string="sqlite:///sales_warehouse.db"
)


# ============================================================
# 3. СОЗДАЕМ DATA ASSETS
# ============================================================

reference_asset = pandas_ds.add_csv_asset(
    name="reference_data",
    filepath_or_buffer="historical_sales.csv",
)

sql_asset = sqlite_ds.add_table_asset(
    name="daily_sales",
    table_name="daily_sales",
)


# ============================================================
# 4. АВТОПРОФИЛИРОВАНИЕ (Data Assistant)
# ============================================================

# Получаем batch request для reference данных
batch_request = reference_asset.build_batch_request()

# Запускаем Data Assistant
assistant_result = context.assistants.onboarding.run(
    batch_request=batch_request,
    estimation="exact"
)

# Получаем и сохраняем expectation suite
suite = assistant_result.get_expectation_suite("reference_suite")
context.add_expectation_suite(expectation_suite=suite)


# ============================================================
# 5. ДОБАВЛЕНИЕ РУЧНЫХ ОЖИДАНИЙ
# ============================================================

# Получаем suite для редактирования
suite = context.get_expectation_suite("reference_suite")

# Добавляем expectations с правильными названиями
suite.add_expectation(
    gx.core.ExpectationConfiguration(
        expectation_type="expect_column_values_to_not_be_null",
        kwargs={"column": "amount"},
    )
)

suite.add_expectation(
    gx.core.ExpectationConfiguration(
        expectation_type="expect_column_values_to_be_between",
        kwargs={"column": "amount", "min_value": 0, "strict_min": True},
    )
)

suite.add_expectation(
    gx.core.ExpectationConfiguration(
        expectation_type="expect_column_values_to_match_regex",
        kwargs={
            "column": "user_email",
            "regex": r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
        },
    )
)

context.update_expectation_suite(suite)


# ============================================================
# 6. РАСЧЁТ PARTITION OBJECT ДЛЯ KL-ДИВЕРГЕНЦИИ
# ============================================================

df_hist = pd.read_csv("historical_sales.csv")
hist = df_hist["category"].value_counts(normalize=True).to_dict()

partition_object = {
    "values": list(hist.keys()),
    "weights": list(hist.values()),
}

suite.add_expectation(
    gx.core.ExpectationConfiguration(
        expectation_type="expect_column_kl_divergence_to_be_less_than",
        kwargs={
            "column": "category",
            "partition_object": partition_object,
            "threshold": 0.3,
        },
    )
)

context.update_expectation_suite(suite)


# ============================================================
# 7. СОЗДАЕМ CHECKPOINT
# ============================================================

# Создаем batch request для SQL данных
sql_batch_request = sql_asset.build_batch_request()

checkpoint_config = {
    "name": "sales_quality_check",
    "config_version": 1.0,
    "class_name": "SimpleCheckpoint",
    "validations": [
        {
            "batch_request": sql_batch_request,
            "expectation_suite_name": "reference_suite",
        }
    ],
}

context.add_checkpoint(**checkpoint_config)


# ============================================================
# 8. ЗАПУСК ЧЕКПОИНТА
# ============================================================

print("\n=== Запуск чекпоинта ===")
result = context.run_checkpoint(checkpoint_name="sales_quality_check")
print(f"Результат: {result['success']}")


# ============================================================
# 9. СБОРКА DATA DOCS
# ============================================================

context.build_data_docs()

print("\nГотово! Открой файл:")
print("gx/uncommitted/data_docs/local_site/index.html")