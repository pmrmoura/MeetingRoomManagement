from django.db import models
from django.contrib.auth.models import User


class MeetingRoom(models.Model):
    name = models.CharField(max_length=100)


class Reservation(models.Model):
    title = models.CharField(max_length=100)
    from_date = models.DateTimeField()
    to_data = models.DateTimeField()
    employees = models.ManyToManyField(User)
    room = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE)
