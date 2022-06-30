from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from project.pagination import CustomPageNumberPagination

from .models import Product
from .serializers import DetailProductSerializer, ListProductsSerializer
from .mixins import SerializerByMethodMixin
from .permissions import ProductPermissionsCustom

class ListCreateView(SerializerByMethodMixin,generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_map = {
        'GET': ListProductsSerializer,
        'POST': DetailProductSerializer
    }
    pagination_class = CustomPageNumberPagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [ProductPermissionsCustom]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class RetriveUpdateView(SerializerByMethodMixin,generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_map = {
        'GET': ListProductsSerializer,
        'PATCH': DetailProductSerializer
    }

    authentication_classes = [TokenAuthentication]
    permission_classes = [ProductPermissionsCustom]