from rest_framework import serializers
from .models import Role, Otp

from django.contrib.auth.models import User

from django.contrib.auth import get_user_model

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ForgatePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class SavePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('is_staff', 'is_superuser', 'groups', 'user_permissions', 'password')



class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'user_id', 'password', 'name', 'status']
        
    def validate_user_id(self, value):
        if value == '':
            raise serializers.ValidationError("Email cannot be empty.")

        try:
            User.objects.get(user_id=value)
            raise serializers.ValidationError("The email already present")
        except User.DoesNotExist:
            return value

    def create(self, validated_data):
        user = User.objects.create_user(name=validated_data['name'],password=validated_data['password'], user_id=validated_data['user_id'], email=validated_data['email'], status=validated_data['status'])
        return user
