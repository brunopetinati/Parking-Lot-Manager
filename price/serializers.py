from rest_framework import serializers
from .models import PricingModel

class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingModel
        fields = ['id','a_coefficient', 'b_coefficient']

