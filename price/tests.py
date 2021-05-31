from django.test import TestCase
from rest_framework.test import APIClient

class TestPricingView(TestCase):
    def setUp(self):
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

        self.create_parking = {
            "name": "floor 1",
            "fill_priority": 2,
            "motorcycle_spaces": 0,
            "car_spaces": 100,
        }

        self.car_data = {"vehicle_type": "car", "license_plate": "ZYX3269"}

        self.pricing_data = {"a_coefficient": 2, "b_coefficient": 4}


    def test_create_pricing(self):
        client = APIClient()

        user = client.post("/api/accounts/", self.create_user, format="json").json()

        token = client.post("/api/login/", self.superuser_login, format="json").json()[
            "token"
        ]

        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        pricing = client.post("/api/pricings/", self.pricing_data, format="json").json()

        pricing_data = self.pricing_data
        pricing_data["id"] = 1
        self.assertEqual(pricing, pricing_data)

    def test_pricing_rules(self):
        client = APIClient()

        user = client.post("/api/accounts/", self.create_user, format="json").json()

        token = client.post("/api/login/", self.superuser_login, format="json").json()[
            "token"
        ]

        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create pricing but no level
        client.post("/api/pricings/", self.pricing_data, format="json")

        client.post("/api/levels/", self.create_parking, format="json")

        response = client.post("api/vehicles/", self.car_data, format="json")

        self.assertTrue(response.status_code, 404)