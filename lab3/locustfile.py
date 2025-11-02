import time
import uuid
from locust import HttpUser, SequentialTaskSet, task, between

class BlogBehavior(SequentialTaskSet):
    def on_start(self):
        # Генерация имени пользователя
        self.username = f"user_{uuid.uuid4()}"
        self.post_id = None

    @task
    def create_post_and_read(self):
        # Создание нового поста
        response = self.client.post("/posts", json={
            "author": self.username,
            "title": "My new post",
            "content": "This is a test post"
        })
        if response.status_code == 201:
            self.post_id = response.json()["id"]
            # Чтение только что созданного поста
            self.client.get(f"/posts/{self.post_id}")

    @task(5)
    def read_all_posts(self):
        self.client.get("/posts")

    @task(3)
    def read_post_1(self):
        self.client.get("/posts/1")


class BlogUser(HttpUser):
    tasks = [BlogBehavior]
    wait_time = between(1, 3)
