from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Product

class PostProductSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class GetProductsSerializer(serializers.ModelSerializer):
    seller_id = UserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'