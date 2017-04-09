from django.contrib.auth.hashers import make_password

from rest_framework.serializers import ValidationError
from rest_framework import serializers

from django.contrib.auth import get_user_model


User = get_user_model()


class UserVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'verified',
        )
        read_only_fields = ("verified", )
        # extra_kwargs = {
        #     'password': {'write_only': True},
        #     'repeat_password': {'write_only': True},
        # }

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
        # read_only_fields = ("password", )
        extra_kwargs = {
            'password': {'write_only': True},
            'repeat_password': {'write_only': True},
        }

    def validate(self, data):
        if data['repeat_password'] != data['password']:
            raise ValidationError(
                {'repeat_password': "Repeated password doesn't match."})
        return data

    def create(self, data):
        if data.get('password'):
            data['password'] = make_password(data['password'])

        data.pop("repeat_password")
        return super().create(data)
