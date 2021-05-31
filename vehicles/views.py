from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from datetime import datetime, timezone
from django.shortcuts import get_object_or_404

from .models import VehicleModel
from parking.models import SpaceModel, SpaceType
from price.models import PricingModel

from .serializers import VehicleSerializer

from .services import find_paking_all

# Create your views here.


class VehicleEntryView(APIView):
    def post(self, request):

        # verificação se existe precificação
        if not PricingModel.objects.last():
            return Response({'error':'no pricing registered'}, status=status.HTTP_404_NOT_FOUND)

        serializer = VehicleSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.data['vehicle_type'] not in [k for k,v in SpaceType.choices]:
            return Response({'message':'invalid vehicle type'})

        find_space = find_paking_all(request.data['vehicle_type'])

        # caso há vaga, cria um objeto veículo, e atribui a vaga
        if find_space:
            vehicle = VehicleModel.objects.create(**request.data, space=find_space)
            serializer = VehicleSerializer(vehicle)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message':'no parking available'}, status=status.HTTP_404_NOT_FOUND)

class VehicleExitView(APIView):
    def put(self, request, vehicle_id):

        vehicle = get_object_or_404(VehicleModel, pk=vehicle_id)

        # caso o veículo já tenha deixado o estacionamento, e mesmo assim tenta-se aplicar outra saída
        if vehicle.space == None:
            return Response({'error':'vehicle not found'}, status=status.HTTP_404_NOT_FOUND)

        pricing = PricingModel.objects.last()
        amount_paid = pricing.calculate_fee(vehicle)

        vehicle.amount_paid = amount_paid
        vehicle.paid_at = datetime.now(timezone.utc)
        vehicle.space = None

        vehicle.save()

        serializer = VehicleSerializer(vehicle)

        return Response(serializer.data, status=status.HTTP_200_OK)