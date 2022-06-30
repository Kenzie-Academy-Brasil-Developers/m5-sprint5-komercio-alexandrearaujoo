from rest_framework import serializers
from users.serializers import UserSerializer
from django.core.validators import MinValueValidator
from .models import Product

class DetailProductSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {'quantity': {'validators':[MinValueValidator(0)]}}

class ListProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'description', 'price', 'quantity', 'is_active', 'seller_id']