from rest_framework import serializers
from parking.serializers import SpaceSerializer

class VehicleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    license_plate = serializers.CharField()
    vehicle_type = serializers.CharField()
    arrived_at = serializers.DateTimeField(read_only=True)
    paid_at = serializers.DateTimeField(read_only=True)
    amount_paid = serializers.IntegerField(read_only=True)
    space = SpaceSerializer(read_only=True)