"""B8 homework: load test GET /tasks with Bearer authentication."""
import os

from locust import HttpUser, between, task


class TasksUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.client.headers["Authorization"] = (
            f"Bearer {os.environ.get('TASKS_API_TOKEN', 'demo-token')}"
        )

    @task
    def list_tasks(self):
        self.client.get("/tasks?limit=10", name="GET /tasks")

