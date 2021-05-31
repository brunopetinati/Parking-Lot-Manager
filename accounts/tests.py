from django.test import TestCase
from rest_framework.test import APIClient


class TestAccountView(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.create_user = {
            "username": "superuser",
            "password": "1234",
            "is_superuser": True,
            "is_staff": True,
        }

        self.superuser_login = {
            "username": "superuser",
            "password": "1234",
        }

    def test_create_user_and_login(self):
        user = self.client.post("/api/accounts/", self.create_user, format="json").json()

        self.assertDictEqual(
            user, {"id": 1, "username": "superuser", "is_superuser": True, "is_staff": True}
        )

        # login
        response = self.client.post(
            "/api/login/", self.superuser_login, format="json"
        ).json()

        self.assertIn("token", response.keys())

