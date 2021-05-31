# Parking Lot Manager

**Version 1.0.0**

Platform designed to manage parking, in which it's possible to register floor parking, prices and vehicles. The system calculates automatically the hours stayed and generates the total amount to be paid.
This is only the back-end API.

---

## Details

Prices will be calculated using the following formula: Total_Price = a_coefficient + b_coefficient * Delta_Hour(leaving - entering).

## Installation

Create a virtual environment with:
python3 -m venv venv

Enter into your environment:
source venv/bin/activate
cd ParkingLotRes

On the terminal, run

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

---

## Further Information

### Routes
- POST /api/accounts/ - creates users
- POST /api/login/ - authenticates
- POST /api/levels/ - creates floors (only superuser)
- GET /api/levels/ - list all floors and their available spaces
- POST /api/pricings/ - creates pricing. The system will use the last one registered.
- POST /api/vehicles/ - creates vehicle, which automatically alocates vehicle into available space, according to defined priorities.
- PUT /api/vehicles/<int:vehicle_id>/ registers moment that vehicle is leaving the parking lot. It'll generate the price automatically.


### Examples of Requests:

#### Creating superuser

##### POST /api/accounts/

{
  "username": "admin",
  "password": "1234",
  "is_superuser": true,
  "is_staff": true
}


#### Login - Getting token

##### POST /api/login/


{
  "username": "admin",
  "password": "1234"
}

#### Creating parking

##### POST /api/levels/


Header -> Authorization: Token <is_superuser token>

{
  "name": "floor 1",
  "fill_priority": 2,
  "motorcycle_spaces": 20,
  "car_spaces": 50
}

#### Defining pricing

##### POST /api/pricings/


Header -> Authorization: Token <is_superuser token>

{
  "a_coefficient": 100,
  "b_coefficient": 100
}

#### Registering vehicle at arrival moment

##### POST /api/vehicles/


Header -> Authorization: Token <is_superuser token>

{
  "vehicle_type": "car",
  "license_plate": "AYO1029"
}

#### Calculating final price according to staying in

##### PUT /api/vehicles/<int:vehicle_id>/

Header -> Authorization: Token <is_superuser token>
