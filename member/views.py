from rest_framework import generics

from .serializers import UserSerializer, UserVerifySerializer

from django.contrib.auth import get_user_model


User = get_user_model()


class VerifyView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.filter(verified=False)
    serializer_class = UserVerifySerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
