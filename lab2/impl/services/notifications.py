from confluent_kafka import Consumer
import json
import logging

from config import get_settings, Settings

class NotificationService:
    def __init__(
        self, 
        consumer: Consumer, 
        settings: Settings = get_settings()
    ):
        self._consumer = consumer
        self._settings = settings
        
    def start_listening(
        self, 
        delay: float = 1.0, 
        callback=lambda x: logging.info(f"📦 Received: {x}")
    ) -> None:

        self._consumer.subscribe([self._settings.topic_name])
        self.working = True

        while self.working:
            msg = consumer.poll(delay)
            if msg is None:
                continue
            data = json.loads(msg.value())
            callback(data)

        self._consumer.close()

    def stop_listening(self):
        self.working = False
        

