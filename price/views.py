from django.shortcuts import render

from rest_framework import authentication, permissions, status
from rest_framework.response import Response

from rest_framework.generics import ListCreateAPIView


from .serializers import PricingSerializer
from .models import PricingModel

from rest_framework.authentication import TokenAuthentication
from permissions.permissions import AdminAuthorization


class PricingView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminAuthorization]
    queryset = PricingModel.objects.all()
    serializer_class = PricingSerializer
    

    