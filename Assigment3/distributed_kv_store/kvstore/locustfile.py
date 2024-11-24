from locust import HttpUser, task, between

class KeyValueTestUser(HttpUser):
    wait_time = between(1, 5)  # Интервал времени между запросами (в секундах)

    @task(1)
    def get_key_value(self):
        # Тест на получение данных по ключу
        self.client.get("/api/kv/user123/")

    @task(2)
    def post_key_value(self):
        # Тест на создание или обновление данных
        payload = {"key": "user123", "value": "Alice"}
        headers = {"Content-Type": "application/json"}
        self.client.post("/api/kv/", json=payload, headers=headers)
