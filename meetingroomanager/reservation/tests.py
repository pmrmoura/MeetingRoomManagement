import json

from django.urls import reverse
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from reservation.models import MeetingRoom, Reservation


class MeetingRoomTestCase(APITestCase):
    def get_URL(self, type, *args, **kwargs):
        """
        Returns URL in case the test need a list or
        detail
        """
        url_prefix = "reservation:rooms-"
        final_url = url_prefix + type

        if type == "detail":
            self.url = reverse(final_url, kwargs=kwargs["kwargs"])
        else:
            self.url = reverse(final_url)

    def setUp(self):
        self.username = "ronaldo"
        self.password = "ronaldinho"
        self.user = User.objects.create(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.room_data = {
            "name": "testroom",
        }
        self.get_URL("list")

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_not_authenticated_room_creation(self):
        """
        Test to verify that meeting room is not being created
        when user is not authenticated
        """
        response = self.client.post(self.url, self.room_data)
        self.assertEqual(401, response.status_code)

    def test_authenticated_room_creation(self):
        """
        Test to verify that meeting room is being created
        when user is authenticated
        """
        self.api_authentication()
        response = self.client.post(self.url, self.room_data)
        self.assertEqual(201, response.status_code)

    def test_authenticated_room_list(self):
        """
        Test to verify that meeting rooms are listed
        when user is authenticated
        """
        self.api_authentication()
        response = self.client.get(self.url, self.room_data)
        self.assertEqual(200, response.status_code)

    def test_room_deletion(self):
        """
        Test to verify that meeting rooms are deleted
        when user is authenticated
        """
        self.api_authentication()
        test_room = MeetingRoom.objects.create(name="test_room")
        self.get_URL("detail", kwargs={'pk': test_room.id})
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)


class ReservationTestCase(APITestCase):
    def get_URL(self, type, *args, **kwargs):
        """
        Returns URL in case the test need a list or
        detail
        """
        url_prefix = "reservation:reservation-"
        final_url = url_prefix + type

        if type == "detail":
            self.url = reverse(final_url, kwargs=kwargs["kwargs"])
        else:
            self.url = reverse(final_url)

    def setUp(self):
        self.username = "ronaldo"
        self.password = "ronaldinho"
        self.user = User.objects.create(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.room = MeetingRoom.objects.create(name="test_room")
        self.get_URL("list")

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_create_reservation(self):
        """
        Test reservation schedule
        """
        reservation_data = {
            "title": "Deciding2",
            "from_date": "2021-12-14T23:20:05Z",
            "to_data": "2021-12-14T23:20:09Z",
            "room": self.room.id,
            "employees": [self.user.id]
        }
        self.api_authentication()
        response = self.client.post(self.url, reservation_data)
        self.assertEqual(201, response.status_code)

    def test_create_reservation_with_equal_time(self):
        """
        Test the creation of equal date and time reservations
        """
        reservation_data = {
            "title": "Deciding2",
            "from_date": "2021-12-14T23:20:05Z",
            "to_data": "2021-12-14T23:20:09Z",
            "room": self.room.id,
            "employees": [self.user.id]
        }
        first_reservation = Reservation.objects.create(
            title="Deciding2",
            from_date="2021-12-14T23:20:05Z",
            to_data="2021-12-14T23:20:09Z",
            room=self.room,
        )
        first_reservation.employees.set([self.user.id])

        self.api_authentication()
        with self.assertRaises(Exception) as raised:
            self.client.post(self.url, reservation_data)
        self.assertEqual(IntegrityError, type(raised.exception))

    def test_create_reservation_with_overlap_time(self):
        """
        Test the creation of overlapping date and time reservations
        """

        reservation_data = {
            "title": "Deciding2",
            "from_date": "2021-12-12T23:20:05Z",
            "to_data": "2021-12-14T23:20:09Z",
            "room": self.room.id,
            "employees": [self.user.id]
        }
        first_reservation = Reservation.objects.create(
            title="Deciding3",
            from_date="2021-12-11T23:20:05Z",
            to_data="2021-12-14T23:20:09Z",
            room=self.room,
        )
        first_reservation.employees.set([self.user.id])

        self.api_authentication()
        with self.assertRaises(Exception) as raised:
            self.client.post(self.url, reservation_data)
        self.assertEqual(IntegrityError, type(raised.exception))
    
    def test_create_reservation_with_missing_fields(self):
        """
        Test reservation creation with missing fields (title)
        """
        reservation_data = {
            "from_date": "2021-12-14T23:20:05Z",
            "to_data": "2021-12-14T23:20:09Z",
            "room": self.room.id,
            "employees": [self.user.id]
        }
        self.api_authentication()
        response = self.client.post(self.url, reservation_data)
        self.assertEqual(400, response.status_code)

    def test_delete_reservation(self):
        """
        Test to verify that reservations are deleted
        when user is authenticated
        """
        self.api_authentication()
        reservation = Reservation.objects.create(
            title="Deciding3",
            from_date="2021-12-11T23:20:05Z",
            to_data="2021-12-14T23:20:09Z",
            room=self.room,
        )
        reservation.employees.set([self.user.id])
        self.get_URL("detail", kwargs={'pk': reservation.id})
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)