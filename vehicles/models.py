from django.db import models
from parking.models import SpaceModel, SpaceType

# Create your models here.

class VehicleModel(models.Model):
    license_plate = models.CharField(max_length=255)
    vehicle_type = models.CharField(max_length=255, choices=SpaceType.choices)
    arrived_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True)
    amount_paid = models.IntegerField(null=True)
    space = models.OneToOneField(SpaceModel, on_delete=models.CASCADE, null=True)