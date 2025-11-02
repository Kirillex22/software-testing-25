import time
import pytest
from testcontainers.postgres import PostgresContainer
from testcontainers.kafka import KafkaContainer
from config import Settings, set_settings

@pytest.fixture(scope="session")
def containers():
    """Запускаем PostgreSQL и Kafka в Docker"""
    with PostgresContainer("postgres:16") as postgres, KafkaContainer("confluentinc/cp-kafka:7.5.0") as kafka:
        time.sleep(5)
        yield {"postgres": postgres, "kafka": kafka}


@pytest.fixture(scope="session")
def settings(containers):
    """Настройки проекта на основе контейнеров"""
    pg = containers["postgres"]
    kafka = containers["kafka"]
    cfg = Settings(
        database_url=pg.get_connection_url(),
        broker_url=kafka.get_bootstrap_server(),
        topic_name="orders"
    )
    print("Kafka bootstrap server:", kafka.get_bootstrap_server())
    set_settings(cfg)
    yield cfg

# Подключаем фикстуры из папки fixtures
pytest_plugins = [
    "tests.fixtures.db",
    "tests.fixtures.kafka",
]
