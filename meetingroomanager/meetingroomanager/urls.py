from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    # path('api-token-auth/', obtain_auth_token),
    path("auth/", include("authentication.urls")),
]
