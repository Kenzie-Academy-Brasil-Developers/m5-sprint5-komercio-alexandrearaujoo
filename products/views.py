from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from .models import Product
from .serializers import PostProductSerializer, GetProductsSerializer
from .mixins import SerializerByMethodMixin
from .permissions import ProductPermissionsCustom

class ListCreateView(SerializerByMethodMixin,generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_map = {
        'GET': GetProductsSerializer,
        'POST': PostProductSerializer
    }
    authentication_classes = [TokenAuthentication]
    permission_classes = [ProductPermissionsCustom]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class RetriveUpdateView(SerializerByMethodMixin,generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_map = {
        'GET': GetProductsSerializer,
        'PATCH': PostProductSerializer
    }

    authentication_classes = [TokenAuthentication]
    permission_classes = [ProductPermissionsCustom]