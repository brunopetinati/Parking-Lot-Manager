from django.test import TestCase
from rest_framework.test import APIClient

class TestParkingView(TestCase):
    def setUp(self):
        self.superuser = {
            "username": "superuser",
            "password": "1234",
            "is_superuser": True,
            "is_staff": True,
        }

        self.superuser_login = {
            "username": "superuser",
            "password": "1234",
        }

        self.parking_data = {
            "name": "floor 1",
            "fill_priority": 1,
            "motorcycle_spaces": 10,
            "car_spaces": 20,
        }

    def test_create_parking(self):
        client = APIClient()

        user = client.post("/api/accounts/", self.superuser, format="json").json()

        token = client.post("/api/login/", self.superuser_login, format="json").json()[
            "token"
        ]

        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        parking = client.post("/api/levels/", self.parking_data, format="json").json()

        self.assertEqual(parking["id"], 1)
        self.assertEqual(parking["available_spaces"]["available_motorcycle_spaces"], 10)
        self.assertEqual(parking["available_spaces"]["available_car_spaces"], 20)

    def test_get_parking(self):
        client = APIClient()

        user = client.post("/api/accounts/", self.superuser, format="json").json()

        token = client.post("/api/login/", self.superuser_login, format="json").json()[
            "token"
        ]

        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create 2 levels
        parking = client.post("/api/levels/", self.parking_data, format="json").json()

        parking = client.post("/api/levels/", self.parking_data, format="json").json()

        list_parking = client.get("/api/levels/").json()

        self.assertEqual(len(list_parking), 2)

        for i, parking in enumerate(list_parking):
            self.assertEqual(parking["id"], i + 1)
            self.assertEqual(
                parking["available_spaces"]["available_motorcycle_spaces"], 10
            )
            self.assertEqual(parking["available_spaces"]["available_car_spaces"], 20)