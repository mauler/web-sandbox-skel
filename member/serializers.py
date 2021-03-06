from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, get_user_model
from django.utils.http import urlsafe_base64_decode

from rest_framework.serializers import ValidationError
from rest_framework import serializers

from .models import Team

User = get_user_model()


class InviteSerializer(serializers.Serializer):
    invite_code = serializers.CharField()


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("name", )


class ResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    repeat_password = serializers.CharField()

    def validate(self, data):
        if data['repeat_password'] != data['password']:
            raise ValidationError(
                {'repeat_password': "Repeated password doesn't match."})
        return data


class ResetChangePasswordSerializer(ChangePasswordSerializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        data = super().validate(data)
        user_pk = urlsafe_base64_decode(data['uidb64'])
        user = User.objects.get(pk=user_pk)

        form = SetPasswordForm(
            user,
            data={'new_password1': data['password'],
                  'new_password2': data['password']})
        if not form.is_valid():
            raise ValidationError(form.errors)

        if not default_token_generator.check_token(user, data['token']):
            raise ValidationError({'token': ['Invalid token']})

        data['user_pk'] = user.pk
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user is None:
            raise ValidationError("Wrong credentials")
        else:
            data['user'] = user
            return data


class UserVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'verified',
        )
        read_only_fields = ("verified", )

    def update(self, instance, validated_data):
        instance.verified = True
        return instance


class UserSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(max_length=128,
                                            write_only=True)

    invite_code = serializers.CharField(write_only=True,
                                        required=False,
                                        allow_null=True)
    team = TeamSerializer(required=False)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
            'repeat_password',
            'team',
            'invite_code',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_invite_code(self, value):
        try:
            user_pk = urlsafe_base64_decode(value)
            qs = User.objects.filter(pk=user_pk)
        except ValueError:
            raise ValidationError("Invalid invite code.")
        else:
            if not qs.exists():
                raise ValidationError("Invalid invite code.")
            return int(user_pk)

        return value

    def validate(self, data):
        if data['repeat_password'] != data['password']:
            raise ValidationError(
                {'repeat_password': "Repeated password doesn't match."})
        data.pop('repeat_password')
        data['team_id'] = data.pop('invite_code', None)
        data['password'] = make_password(data['password'])
        return data
