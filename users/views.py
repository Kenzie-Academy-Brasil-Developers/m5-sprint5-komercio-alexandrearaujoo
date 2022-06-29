from rest_framework import generics
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView, Response, status

from .serializers import LoginSerializer, UserSerializer

from .permissions import UserPermissionsCustom

from .models import User


class ListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ListUsersDateJoinedView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
      num_users = self.kwargs["num"]
      return self.queryset.order_by("-date_joined")[0:num_users]

class UpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [UserPermissionsCustom]


class LoginView(APIView):
    def post(self, request): 
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(username=email, password=password)

        if user: 
            token, _ = Token.objects.get_or_create(user=user)

            return Response({"token": token.key}, status.HTTP_200_OK)

        return Response(
            {"detail": "invalid email or password"},
            status.HTTP_401_UNAUTHORIZED
        )