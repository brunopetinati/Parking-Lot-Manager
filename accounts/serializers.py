from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_staff', 'is_superuser', 'username', 'password', 'id']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class CredentialSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()