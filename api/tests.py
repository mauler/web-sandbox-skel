from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model


User = get_user_model()


class ResetChangePasswordTests(APITestCase):
    RESET_CHANGE_PASSWORD_URL = reverse('member:reset_change_password')

    def setUp(self):
        self.user = User.objects.create(email="proberto.macedo@gmail.com")
        self.user.set_unusable_password()
        self.user.save(update_fields=['password'])
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk)).decode()
        self.token = default_token_generator.make_token(self.user)

    def test_reset(self):
        data = {
            "uidb64": self.uid,
            "token": self.token,
            "password": "new12345",
            "repeat_password": "new12345",
        }
        response = self.client.post(
            self.RESET_CHANGE_PASSWORD_URL,
            data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})
        user = User.objects.get(pk=self.user.pk)
        self.assertTrue(
            user.has_usable_password())
        self.assertIsNotNone(authenticate(
            email="proberto.macedo@gmail.com",
            password=data['password']))


class ResetTests(APITestCase):
    RESET_PASSWORD_URL = reverse('member:reset_password')

    def setUp(self):
        self.user = User.objects.create(email="proberto.macedo@gmail.com")

    def test_reset(self):
        response = self.client.post(
            self.RESET_PASSWORD_URL,
            {'email': self.user.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})
        self.assertFalse(
            User.objects.get(pk=self.user.pk).has_usable_password())

    def test_reset_unexistent_email(self):
        response = self.client.post(
            self.RESET_PASSWORD_URL,
            {'email': "foobar@invalid.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})


class PasswordTests(APITestCase):
    CHANGE_PASSWORD_URL = reverse('member:change_password')
    RESET_PASSWORD_URL = reverse('member:change_password')
    PASSWORD_SAMPLE = {
        "password": "change1234",
        "repeat_password": "change1234",
    }

    def setUp(self):
        self.user = User.objects.create(email="proberto.macedo@gmail.com")

    def test_change_password(self):
        self.client.force_login(self.user)
        response = self.client.put(
            self.CHANGE_PASSWORD_URL,
            self.PASSWORD_SAMPLE.copy())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})
        self.assertIsNotNone(authenticate(
            email="proberto.macedo@gmail.com",
            password='change1234'))

    def test_password_change_unauthenticated(self):
        response = self.client.put(
            self.CHANGE_PASSWORD_URL,
            self.PASSWORD_SAMPLE.copy())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data,
            {'detail': 'Authentication credentials were not provided.'})


class LoginTests(APITestCase):
    LOGIN_URL = reverse('member:login')
    LOGIN_SAMPLE = {
        "email": "proberto.macedo@gmail.com",
        "password": "pwd1234",
    }

    def setUp(self):
        self.user = User.objects.create(
            email="proberto.macedo@gmail.com",
            verified=True)
        self.user.set_password('pwd1234')
        self.user.save(update_fields=['password'])

    def test_login(self):
        response = self.client.post(
            self.LOGIN_URL,
            self.LOGIN_SAMPLE.copy())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})


class VerifyTests(APITestCase):

    def test_verify(self):
        user = User.objects.create(email="proberto.macedo@gmail.com")
        url = reverse("member:verify", args=(user.pk, ))
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'verified': True})

    def test_verify_validate_already_verified(self):
        """ Quite unecessary since this doesn't change anything, but just to
        ilustrate the VerifyView queryset validated. """
        user = User.objects.create(email="proberto.macedo@gmail.com",
                                   verified=True)
        url = reverse("member:verify", args=(user.pk, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RegisterTests(APITestCase):
    REGISTER_URL = reverse('member:register')
    REGISTER_SAMPLE = {
        'email': "proberto.macedo@gmail.com",
        'password': "register1234",
        'repeat_password': "register1234",
        'first_name': "Paulo",
        'last_name': "Developer",
    }

    def test_register_validate_repeat_password(self):
        data = self.REGISTER_SAMPLE.copy()
        data.update({'repeat_password': 'invalid'})
        response = self.client.post(self.REGISTER_URL, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'repeat_password': ["Repeated password doesn't match."]})

    def test_register(self):
        response = self.client.post(self.REGISTER_URL, self.REGISTER_SAMPLE)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {'email': 'proberto.macedo@gmail.com',
             'first_name': 'Paulo',
             'last_name': 'Developer'})

        qs = User.objects.all()
        self.assertQuerysetEqual(qs, ['<User: proberto.macedo@gmail.com>'])

        user = qs.get()
        self.assertEqual(user.first_name, "Paulo")
        self.assertEqual(user.last_name, "Developer")
        self.assertFalse(user.verified,
                         "Registered user should be unverified.")
        self.assertIsNone(user.team,
                          "Uninvited users should not be part of a team.")
