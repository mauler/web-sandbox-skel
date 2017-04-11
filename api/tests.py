from django.contrib.auth import authenticate
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model


User = get_user_model()


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

    # def test_reset_needs_authentication(self):
    #     user = User.objects.create(email="proberto.macedo@gmail.com")
    #     url = reverse("member:verify", args=(user.pk, ))
    #     response = self.client.put(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data, {'verified': True})

    # def test_reset(self):
    #     user = User.objects.create(email="proberto.macedo@gmail.com")
    #     url = reverse("member:verify", args=(user.pk, ))
    #     response = self.client.put(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data, {'verified': True})

    # def test_verify_validate_already_verified(self):
    #     """ Quite unecessary since this doesn't change anything, but just to
    #     ilustrate the VerifyView queryset validated. """
    #     user = User.objects.create(email="proberto.macedo@gmail.com",
    #                                verified=True)
    #     url = reverse("member:verify", args=(user.pk, ))
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class LoginTests(APITestCase):
    LOGIN_URL = reverse('member:login')
    LOGIN_SAMPLE = {
        "email:": "proberto.macedo@gmail.com",
        "password:": "pwd1234",
    }

    def setUp(self):
        self.user = User.objects.create(email="proberto.macedo@gmail.com")
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

    # def test_register_validate_required_fields(self):
    #     data = self.REGISTER_SAMPLE.copy()
    #     data = dict.fromkeys(data.keys(), '')
    #     response = self.client.post(self.REGISTER_URL, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(
    #         response.data,
    #         {'email': ['This field may not be blank.'],
    #          'first_name': ['This field may not be blank.'],
    #          'last_name': ['This field may not be blank.'],
    #          'password': ['This field may not be blank.'],
    #          'repeat_password': ['This field may not be blank.']})

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
