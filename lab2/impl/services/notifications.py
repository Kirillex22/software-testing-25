from confluent_kafka import Consumer
import json

from config import get_settings, Settings

class NotificationService:
    def __init__(
        self, 
        consumer: Consumer, 
        settings: Settings = get_settings()
    ):
        self._consumer = consumer
        self._settings = settings
        self.received = []
        
    def start_listening(
        self, 
        delay: float = 1.0, 
        callback=lambda x: print(f"📦 Received: {x}")
    ) -> None:

        self.working = True

        while self.working:
            msg = self._consumer.poll(delay)
            if msg is None:
                continue
            if msg.error():
                print(f"Error: {msg.error()}")
                continue
            data = json.loads(msg.value())
            callback(data)
            self.received.append(data)

    def stop_listening(self):
        self.working = False
        

