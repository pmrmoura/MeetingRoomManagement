from rest_framework import routers
from .views import MeetingRoomViewSet, ReservationViewSet

app_name = "reservation"

router = routers.DefaultRouter()
router.register("rooms", MeetingRoomViewSet, basename="rooms")
router.register("reservation", ReservationViewSet, basename="reservation")

urlpatterns = router.urls
