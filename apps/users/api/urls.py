from django.urls import path

from apps.users.api import views

app_name = "users_app"

urlpatterns = [
    path("login/", views.LoginUserAPIView.as_view(), name="login"),
    path("refresh/", views.RefreshUserAPIView.as_view(), name="refresh"),
]
