import json
from uuid import uuid4
from confluent_kafka import Consumer
from impl.services.orders import take_order
from impl.services.notifications import NotificationService
from impl.views.order import OrderView
from impl.orm.order import Order

# ============================
# Тесты
# ============================

def test_take_order_saves_and_sends(db_session, kafka_producer, kafka_consumer):
    """Проверяем сохранение заказа в БД и публикацию в Kafka"""
    order_view = OrderView(
        id=str(uuid4()),
        item_name="Keyboard",
        quantity=3
    )

    take_order(order_view, kafka_producer, db_session)

    # Проверяем БД
    saved_order = db_session.query(Order).filter_by(item_name="Keyboard").first()
    assert saved_order is not None
    assert saved_order.quantity == 3

    # Проверяем Kafka
    msg = kafka_consumer.poll(5.0)
    assert msg is not None
    data = json.loads(msg.value())
    assert data["item_name"] == "Keyboard"
    assert data["quantity"] == 3


def test_notification_service_receives_messages(settings, kafka_producer):
    """Проверяем, что NotificationService получает сообщение"""
    consumer = Consumer({
        'bootstrap.servers': settings.broker_url,
        'group.id': 'notif-test',
        'auto.offset.reset': 'earliest'
    })
    service = NotificationService(consumer, settings=settings)

    received = []

    def callback(data):
        received.append(data)

    # Отправляем сообщение
    message = {"event": "order_created", "id": str(uuid4()), "item_name": "Mouse"}
    kafka_producer.produce(settings.topic_name, json.dumps(message).encode("utf-8"))
    kafka_producer.flush()

    service._consumer.subscribe([settings.topic_name])
    msg = service._consumer.poll(5.0)
    assert msg is not None

    payload = json.loads(msg.value())
    callback(payload)

    assert len(received) == 1
    assert received[0]["event"] == "order_created"
    assert received[0]["item_name"] == "Mouse"

    service._consumer.close()
