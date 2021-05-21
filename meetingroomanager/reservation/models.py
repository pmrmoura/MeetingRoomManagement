from django.db import models
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import (
    DateTimeRangeField,
    RangeBoundary,
    RangeOperators,
)
from django.db.models import Func
from django.contrib.auth.models import User


class TsTzRange(Func):
    function = "TSTZRANGE"
    output_field = DateTimeRangeField()


class MeetingRoom(models.Model):
    name = models.CharField(max_length=100)


class Reservation(models.Model):
    title = models.CharField(max_length=100)
    from_date = models.DateTimeField()
    to_data = models.DateTimeField()
    employees = models.ManyToManyField(User)
    room = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            ExclusionConstraint(
                name="exclude_overlapping_reservations",
                expressions=(
                    (
                        TsTzRange("from_date", "to_data", RangeBoundary()),
                        RangeOperators.OVERLAPS,
                    ),
                    ("room", RangeOperators.EQUAL),
                ),
            ),
        ]
