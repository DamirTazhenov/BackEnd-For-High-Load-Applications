from locust import HttpUser, task, between


class UserBehavior(HttpUser):
    # Устанавливаем задержку между запросами (от 1 до 5 секунд)
    wait_time = between(1, 5)

    @task
    def test_api_profile(self):
        self.client.get("/api/profile/edit")

    @task(1)
    def test_login(self):
        self.client.post("/api/token/", {"username": "damir", "password": "Password123!"})

    # @task(2)
    # def test_user_profile(self):
    #     headers = {"Authorization": "Bearer <your_jwt_token>"}
    #     self.client.get("/api/user-profile/", headers=headers)