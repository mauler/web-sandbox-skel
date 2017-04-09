from rest_framework import generics

from .serializers import UserSerializer

from django.contrib.auth import get_user_model


User = get_user_model()


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
