from rest_framework.response import Response
from rest_framework import status

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from .serializers import UserSerializer, CredentialSerializer

class AccountCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = CredentialSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=request.data['username'], password=request.data['password'])

        if user is not None:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({'token': token.key})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)