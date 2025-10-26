import json
import threading
import time
import factory
import pytest
from uuid import uuid4
from confluent_kafka import Consumer
from impl.views.order import OrderView
from impl.orm.order import Order
from impl.services.orders import take_order
from impl.services.notifications import NotificationService
from config import get_settings

settings = get_settings()

# ============================
# Factory-Boy для OrderView
# ============================
class OrderViewFactory(factory.Factory):
    class Meta:
        model = OrderView

    id = factory.LazyFunction(lambda: str(uuid4()))
    item_name = factory.Faker("word")
    quantity = factory.Faker("random_int", min=1, max=10)

# ============================
# Единый интеграционный тест
# ============================
def test_order_flow(db_session, kafka_producer, kafka_consumer):
    """Интеграционный тест: take_order -> БД -> NotificationService"""
    # 1. Создаем заказ через фабрику
    order_view = OrderViewFactory()

    # 2. Настраиваем Kafka Consumer для NotificationService
    notification_service = NotificationService(kafka_consumer)

    # 3. Запускаем NotificationService в отдельном потоке
    t = threading.Thread(target=notification_service.start_listening, kwargs={'delay': 0.5})
    t.start()
    time.sleep(1)  # даем потоку время на подписку

    # 4. Отправляем заказ через сервис
    take_order(order_view, kafka_producer, db_session)

    # 5. Проверяем БД
    saved_order = db_session.query(Order).filter_by(id=order_view.id).first()
    assert saved_order is not None
    assert saved_order.item_name == order_view.item_name
    assert saved_order.quantity == order_view.quantity

    # 6. Ждем, пока NotificationService получит сообщение
    timeout = 5
    start_time = time.time()
    while not notification_service.received and (time.time() - start_time) < timeout:
        time.sleep(0.1)

    # 7. Проверяем сообщение
    assert len(notification_service.received) == 1
    received_msg = notification_service.received[0]
    assert received_msg["id"] == str(order_view.id)
    assert received_msg["item_name"] == order_view.item_name

    # 8. Останавливаем сервис
    notification_service.stop_listening()
    t.join()
