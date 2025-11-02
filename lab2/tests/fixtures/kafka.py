import pytest
from confluent_kafka import Producer, Consumer

@pytest.fixture(scope="session")
def kafka_producer(settings):
    producer = Producer({'bootstrap.servers': settings.broker_url})
    yield producer
    producer.flush()


@pytest.fixture(scope="session")
def kafka_consumer(settings):
    consumer = Consumer({
        'bootstrap.servers': settings.broker_url,
        'group.id': 'test-group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([settings.topic_name])
    yield consumer
    consumer.close()
