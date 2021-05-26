from django.db import models
from datetime import datetime, timezone

# Create your models here.

class PricingModel(models.Model):
    a_coefficient = models.IntegerField()
    b_coefficient = models.IntegerField()
    
    
    # método da model
    def calculate_fee(self, vehicle):
        delta = datetime.now(timezone.utc) - vehicle.arrived_at
        seconds_elapsed = delta.total_seconds()
        hour_elapsed = round(seconds_elapsed/3600)

        amount_due = self.a_coefficient + self.b_coefficient * hour_elapsed

        return amount_due
