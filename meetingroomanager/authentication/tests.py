import json

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class UserRegistrationAPIViewTestCase(APITestCase):
    url = reverse("authentication:register")

    def test_user_registration(self):
        """
        Test to verify that a post call with user valid data
        """
        user_data = {
            "username": "testuser",
            "password": "123123",
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(201, response.status_code)
        self.assertTrue("token" in json.loads(response.content))

    def test_user_registration_without_field(self):
        """
        Test to verify if registration fails after send request without
        one of the required fields
        """
        user_data = {"username": "testuser"}
        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code)

    def test_equal_username_registration(self):
        """
        Test if equal usernames can be registered
        """
        user_data = {"username": "testuser", "password": "testpassword"}

        response = self.client.post(self.url, user_data)
        self.assertEqual(201, response.status_code)

        user_data2 = {"username": "testuser", "password": "testpassword2"}

        response = self.client.post(self.url, user_data2)
        self.assertEqual(400, response.status_code)


class UserLoginViewTestCase(APITestCase):
    url = reverse("authentication:login")

    def setUp(self):
        self.username = "ronaldo"
        self.password = "ronaldinho"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )

        self.user.save()

    def test_authentication_without_one_field(self):
        """
        Test if user can login without password
        """
        user_data = {"username": "testuser"}

        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code)

    def test_with_valid_credentials(self):
        """
        Test login with valid credentials
        """
        user_data = {"username": self.username, "password": self.password}

        response = self.client.post(self.url, user_data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("auth_token" in json.loads(response.content))

    def test_with_wrong_password(self):
        """
        Test login with wrong password
        """
        response = self.client.post(
            self.url, {"username": self.username, "password": "neymar"}
        )
        self.assertEqual(400, response.status_code)


class UserTokenAPIViewTestCase(APITestCase):
    url = reverse("authentication:logout")

    def setUp(self):
        self.username = "ronaldo"
        self.password = "ronaldinho"
        self.user = User.objects.create(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def tearDown(self):
        self.user.delete()
        self.token.delete()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_delete_by_key(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)
        self.assertFalse(Token.objects.filter(key=self.token.key).exists())
