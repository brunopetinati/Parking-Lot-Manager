from rest_framework import serializers
from .models import SpaceType

import ipdb

class ParkingSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField
    fill_priority = serializers.IntegerField()
    car_spaces = serializers.IntegerField(write_only=True)
    motorcycle_spaces = serializers.IntegerField(write_only=True)

    available_spaces = serializers.SerializerMethodField('get_available_spaces', read_only=True)

    def get_available_spaces(self, level):

        # aqui pediu vehiclemodel ao invés de vehicle
        # revisar aqui

        available_morotcycle_spaces = len(level.spacemodel_set.filter(
            variety = SpaceType.MOTORCYCLE, vehiclemodel=None
        ))
        available_car_spaces= len(level.spacemodel_set.filter(
            variety = SpaceType.CAR, vehiclemodel=None
        ))

        return {'available_motorcycle_spaces':available_morotcycle_spaces, 'available_car_spaces':available_car_spaces}
        

class SpaceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    variety = serializers.CharField()
    level_name = serializers.SerializerMethodField('get_parking')

    def get_parking(self, space):
        
        # no retorno, o space corresponde ao objeto  {'id': 23, 'variety': 'car', 'level_id': 1}
        # e o level corresponde ao objeto {'id': 1, 'name': 'floor 3b', 'fill_priority': 3}

        return space.level.name