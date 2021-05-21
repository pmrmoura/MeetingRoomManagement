import logging

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import MeetingRoom, Reservation
from .serializers import MeetingRoomSerializer, ReservationSerializer

logger = logging.getLogger("django")


class MeetingRoomViewSet(ModelViewSet):
    serializer_class = MeetingRoomSerializer
    queryset = MeetingRoom.objects.all()
    permission_classes = (IsAuthenticated,)


class ReservationViewSet(ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        query_set = Reservation.objects.all()
        employee_id = self.request.query_params.get("employee_id", None)
        meeting_room_id = self.request.query_params.get("meeting_room_id", None)

        if employee_id is not None:
            logger.info("Filtering reservations by employee")
            query_set = query_set.filter(employees__id=employee_id)

        if meeting_room_id is not None:
            logger.info("Filtering reservations by meeting room")
            query_set = query_set.filter(room__id=meeting_room_id)

        return query_set
