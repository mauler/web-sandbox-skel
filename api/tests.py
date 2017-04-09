from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model


User = get_user_model()


class AccountTests(APITestCase):
    REGISTER_URL = reverse('member:register')
    REGISTER_SAMPLE = {
        'email': "proberto.macedo@gmail.com",
        'password': "register1234",
        'repeat_password': "register1234",
        'first_name': "Paulo",
        'last_name': "Developer",
    }

    def test_register(self):
        response = self.client.post(self.REGISTER_URL, self.REGISTER_SAMPLE)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        qs = User.objects.all()
        self.assertQuerysetEqual(qs, ['<User: proberto.macedo@gmail.com>'])

        user = qs.get()
        self.assertEqual(user.first_name, "Paulo")
        self.assertEqual(user.last_name, "Developer")
        self.assertFalse(user.verified,
                         "Registered user should be unverified.")
        self.assertIsNone(user.team,
                          "Uninvited users should not be part of a team.")
