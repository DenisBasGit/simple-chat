from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "api"
urlpatterns = router.urls

urlpatterns += [
    path("users/", include("apps.users.api.urls", namespace="users_app")),
    path("chat/", include("apps.chat.api.urls", namespace="chat_app")),
]
