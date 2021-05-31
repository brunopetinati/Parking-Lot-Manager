from django.test import TestCase
from rest_framework.test import APIClient

# Create your tests here.
# linha 141 importante; exemplo de subset

class TestVehicleView(TestCase):
    def setUp(self):
        self.create_superuser = {
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

        self.create_parking_2 = {
            "name": "floor 1",
            "fill_priority": 2,
            "motorcycle_spaces": 1,
            "car_spaces": 2,
        }

        self.pricing_data = {"a_coefficient": 2, "b_coefficient": 4}

        self.car_data = {"vehicle_type": "car", "license_plate": "ZYX3163"}

        self.motorcycle_data = {
            "vehicle_type": "motorcycle",
            "license_plate": "FFF-2030",
        }

    def test_create_vehicle_without_parking_results_404(self):
        client = APIClient()

        user = client.post("/api/accounts/", self.create_superuser, format="json").json()

        token = client.post("/api/login/", self.superuser_login, format="json").json()[
            "token"
        ]

        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create pricing but no level
        client.post("/api/pricings/", self.pricing_data, format="json")

        response = client.post("api/vehicles/", self.car_data, format="json")

        self.assertTrue(response.status_code, 404)

    def test_create_vehicle_without_pricing_results_404(self):
        client = APIClient()

        user = client.post("/api/accounts/", self.create_superuser, format="json").json()

        token = client.post("/api/login/", self.superuser_login, format="json").json()[
            "token"
        ]

        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # create level but no pricing
        level = client.post("/api/levels/", self.create_parking, format="json").json()

        response = client.post("/api/vehicles/", self.car_data, format="json")

        self.assertEqual(response.status_code, 404)

    def test_create_vehicle(self):
        client = APIClient()

        user = client.post("/api/accounts/", self.create_superuser, format="json").json()

        token = client.post("/api/login/", self.superuser_login, format="json").json()[
            "token"
        ]

        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        parking = client.post("/api/levels/", self.create_parking, format="json").json()

        pricing = client.post("/api/pricings/", self.pricing_data, format="json")

        car = client.post("/api/vehicles/", self.car_data, format="json").json()

        self.assertDictContainsSubset(
            {
                "license_plate": "ZYX3163",
                "vehicle_type": "car",
                "paid_at": None,
                "amount_paid": None,
                "space": {"id": 1, "variety": "car", "level_name": "floor 1"},
            },
            car,
        )

        # only one parking space left
        parking = client.get("/api/levels/").json()[0]
        available_spaces = parking["available_spaces"]["available_car_spaces"]
        self.assertEqual(available_spaces, 99)

    def test_cars_and_motorcycles_take_different_spaces(self):
        client = APIClient()

        user = client.post("/api/accounts/", self.create_superuser, format="json").json()

        token = client.post("/api/login/", self.superuser_login, format="json").json()[
            "token"
        ]

        client.credentials(HTTP_AUTHORIZATION="Token " + token)

        parking = client.post("/api/levels/", self.create_parking_2, format="json").json()

        pricing = client.post("/api/pricings/", self.pricing_data, format="json")

        car = client.post("/api/vehicles/", self.car_data, format="json").json()

        self.assertDictContainsSubset(
            {
                "license_plate": "ZYX3163",
                "vehicle_type": "car",
                "paid_at": None,
                "amount_paid": None,
            },
            car,
        )


        # ***IMPORTANTE*** para ler Subset dentro de um request

        self.assertDictContainsSubset(
            {"variety": "car", "level_name": "floor 1"}, car["space"]
        )

        # only one parking space left
        parking = client.get("/api/levels/").json()[0]
        available_car_spaces = parking["available_spaces"]["available_car_spaces"]

        self.assertEqual(available_car_spaces, 1)
        available_motorcycle_spaces = parking["available_spaces"][
            "available_motorcycle_spaces"
        ]

        self.assertEqual(available_motorcycle_spaces, 1)

        car = client.post("/api/vehicles/", self.car_data, format="json").json()

        motorcycle = client.post(
            "/api/vehicles/", self.motorcycle_data, format="json"
        ).json()

        parking = client.get("/api/levels/").json()[0]

        available_car_spaces = parking["available_spaces"]["available_car_spaces"]
        available_motorcycle_spaces = parking["available_spaces"][
            "available_motorcycle_spaces"
        ]

        self.assertEqual(available_motorcycle_spaces, 0)
        self.assertEqual(available_car_spaces, 0)
