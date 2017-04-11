from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from rest_framework.serializers import ValidationError
from rest_framework import serializers

from django.contrib.auth import get_user_model


User = get_user_model()


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


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(data['email'], data['password'])
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

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
            'repeat_password',
        )
        extra_kwargs = {
            'password': {'write_only': True},
            # 'repeat_password': {'write_only': True},
        }

    def validate(self, data):
        if data['repeat_password'] != data['password']:
            raise ValidationError(
                {'repeat_password': "Repeated password doesn't match."})
        data.pop('repeat_password')
        data['password'] = make_password(data['password'])
        return data
