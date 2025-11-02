from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from confluent_kafka import Producer
from functools import wraps
import json

from impl.views.order import OrderView
from impl.mappers import map_order_view_to_orm
from config import get_settings, Settings

def send_message(producer: Producer, topic: str, message: dict):
    producer.produce(topic, json.dumps(message).encode('utf-8'))
    producer.flush()

def take_order(order: OrderView, producer: Producer, session: Session) -> None:
    order_orm = map_order_view_to_orm(order)
    session.add(order_orm)
    send_message(producer, get_settings().topic_name, order.to_dict())


