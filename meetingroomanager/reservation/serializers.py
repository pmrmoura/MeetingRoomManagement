import logging

from rest_framework import serializers

from .models import MeetingRoom
from .models import Reservation

logger = logging.getLogger("django")


class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"

    def validate(self, attributes):
        start_date = attributes["from_date"]
        end_date = attributes["to_data"]

        logger.info("Validating dates")

        are_dates_valid = self.check_dates(start_date, end_date)

        if not are_dates_valid:
            raise serializers.ValidationError("end_date must be bigger than start_date")

        logger.info("Dates validated")

        return attributes

    def check_dates(self, start_date, end_date):
        if end_date > start_date:
            return True
        else:
            return False
