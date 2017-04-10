from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from rest_framework.serializers import ValidationError
from rest_framework import serializers

from django.contrib.auth import get_user_model


User = get_user_model()


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


class UserSerializer(ChangePasswordSerializer):

    class Meta(ChangePasswordSerializer.Meta):
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
            'repeat_password',
        )

    # def create(self, data):
    #     if data.get('password'):
    #         data['password'] = make_password(data['password'])

    #     data.pop("repeat_password")
    #     return super().create(data)
