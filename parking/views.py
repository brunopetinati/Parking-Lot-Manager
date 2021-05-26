from django.shortcuts import render

from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


from .serializers import ParkingSerializer
from .models import ParkingModel, SpaceModel, SpaceType


from permissions.permissions import AdminAuthorization
from rest_framework.authentication import TokenAuthentication

# Create your views here.

class ParkingView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminAuthorization]

    def post(self, request):
        serializer = ParkingSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

        create_parking = ParkingModel.objects.create(fill_priority=request.data['fill_priority'], 
        name=request.data['name']
        )


        for _ in range(request.data['motorcycle_spaces']):
            SpaceModel.objects.create(level=create_parking, variety=SpaceType.MOTORCYCLE)
        
        for _ in range(request.data['car_spaces']):
            SpaceModel.objects.create(level=create_parking, variety=SpaceType.CAR)


        serializer = ParkingSerializer(create_parking)


        return Response(serializer.data, status=status.HTTP_201_CREATED)   

    def get(self, request):
        queryset = ParkingModel.objects.all()
        serializer = ParkingSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
