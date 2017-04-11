from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import login, get_user_model
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework import generics, status, viewsets

from .models import Team
from .forms import PasswordResetForm
from .serializers import UserSerializer, UserVerifySerializer, \
    ChangePasswordSerializer, LoginSerializer, ResetSerializer, \
    ResetChangePasswordSerializer, TeamSerializer, InviteSerializer


User = get_user_model()


class InviteView(APIView):
    """
    get:
    Return authenticated user invite code to others register and join the team.
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = InviteSerializer

    def get(self, request, *args, **kwargs):
        """
        Returns logged user invite code to be used on user registration.
        """
        uidb64 = urlsafe_base64_encode(force_bytes(request.user.pk)).decode()
        serializer = self.serializer_class(data={
            'invite_code': uidb64,
        })
        assert serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeamViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the logged user current team.

    post:
    Create a new team and associate it for the current user.
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    def post(self, request, pk=None):
        if request.user.team is not None:
            raise ValidationError("User already have a team.")

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            team = serializer.save()
            request.user.team = team
            request.user.save(update_fields=['team'])
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        team = get_object_or_404(Team, members=request.user)
        serializer = self.serializer_class(team)
        return Response(serializer.data)


class ResetChangePasswordView(APIView):
    """
    post:
    Changes unauthenticated user password using a token and uid previously
    sent by email.
    """
    def post(self, request, *args, **kwargs):
        serializer = ResetChangePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            form = SetPasswordForm(
                user=User.objects.get(pk=serializer.validated_data['user_pk']),
                data={
                    'new_password1': serializer.validated_data['password'],
                    'new_password2': serializer.validated_data['password']})
            assert form.is_valid()
            form.save()
            data = {}
        else:
            data = serializer.data

        return Response(data, status=status.HTTP_200_OK)


class ResetView(APIView):
    """
    post:
    Emails user reset link with token and uid encoded.
    """
    def post(self, request, *args, **kwargs):
        serializer = ResetSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            form = PasswordResetForm(data=serializer.data)
            assert form.is_valid()
            form.save()
            data = {}
        else:
            data = serializer.validated_data

        return Response(data, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    """
    put:
    Changes authenticated user password.
    """
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = ChangePasswordSerializer(
            data=request.data)

        if serializer.is_valid(raise_exception=True):
            user.set_password(serializer.data["password"])
            user.save(update_fields=['password'])
            return Response({}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    post:
    Authenticate on the system.
    """
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            login(request, serializer.validated_data['user'])
            data = {}
        else:
            data = serializer.data

        return Response(data, status=status.HTTP_200_OK)


class VerifyView(generics.RetrieveUpdateAPIView):
    """
    put:
    Verify a user.

    get:
    Check user verified status.
    """
    queryset = User.objects.filter(verified=False)
    serializer_class = UserVerifySerializer


class UserCreateView(generics.CreateAPIView):
    """
    post:
    Register a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
