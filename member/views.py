from django.contrib.auth import login

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from .serializers import UserSerializer, UserVerifySerializer, \
    ChangePasswordSerializer, LoginSerializer

from django.contrib.auth import get_user_model


User = get_user_model()


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=self.request.data)
        if serializer.is_valid():
            login(request, serializer.validated_data['user'])
            data = {}
        else:
            data = serializer.data

        return Response(data, status=status.HTTP_200_OK)


class VerifyView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.filter(verified=False)
    serializer_class = UserVerifySerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
