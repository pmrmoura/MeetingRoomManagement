from django.urls import path

from .views import UserRegistrationAPIView, UserLoginAPIView, UserTokenAPIView

app_name = "authentication"

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="register"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path("logout/", UserTokenAPIView.as_view(), name="logout"),
]
