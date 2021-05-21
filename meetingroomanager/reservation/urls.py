from rest_framework.routers import DefaultRouter
from .views import MeetingRoomViewSet, ReservationViewSet

app_name = "reservation"

router = DefaultRouter()
router.register("rooms", MeetingRoomViewSet, basename="rooms")
router.register("reservation", ReservationViewSet, basename="reservation")

urlpatterns = router.urls
