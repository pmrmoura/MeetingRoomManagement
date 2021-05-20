import logging

from rest_framework import serializers

from .models import MeetingRoom
from .models import Reservation

logger = logging.getLogger("django")


class MeetingRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeetingRoom
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = '__all__'

    def validate(self, attributes):
        room = attributes["room"]
        start_date = attributes["from_date"]
        end_date = attributes["to_date"]
        title = attributes["title"]

        are_dates_valid = self.check_dates(start_date, end_date)

        # if are_dates_valid:
        #     self.check_room_availability(room, start_date, end_date)
        # else:
        #     raise serializers.ValidationError(
        #         "End date must be bigger than start date"
        #     )
        return attributes

    def check_dates(self, start_date, end_date):
        if end_date > start_date:
            return True
        else:
            return False
        
    # def check_room_availability(self, room, start_date, end_date):
