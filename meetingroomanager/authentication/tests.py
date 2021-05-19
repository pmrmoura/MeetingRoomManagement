import json

from django.urls import reverse

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
