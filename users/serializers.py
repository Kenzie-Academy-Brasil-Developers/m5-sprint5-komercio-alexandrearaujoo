from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['email', 'first_name', 'last_name','password','is_seller','date_joined']
        extra_kwargs = {
            'email': {
                'validators':
                [UniqueValidator(queryset=User.objects.all(), message='email already exists')]
            },
            'password': {'write_only': True}
        }

    
    def create (self, validated_data):
        return User.objects.create_user(**validated_data)


class DetailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email', 
            'first_name', 
            'last_name',
            'is_seller',
            'date_joined',
            'is_active'
        ]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255, write_only=True)