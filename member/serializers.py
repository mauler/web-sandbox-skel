from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from django.contrib.auth import get_user_model


User = get_user_model()


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
        read_only_fields = ("password", )
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, data):
        if data.get('password'):
            data['password'] = make_password(data['password'])

        data.pop("repeat_password")
        return super().create(data)
