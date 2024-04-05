from django.urls import path

from apps.chat.api import views

app_name = "chat_app"

urlpatterns = [
    path("thread/", views.ThreadAPIView.as_view(), name="thread"),
    path("thread/<int:pk>/", views.ThreadDetailAPIView.as_view(), name="thread_detail"),
    path("thread/user/<int:user_id>/", views.ThreadUserAPIView.as_view(), name="thread_user"),

    path("thread/<int:pk>/message/", views.ThreadMessageAPIViews.as_view(), name="message"),
    path("message/<int:pk>/read/", views.ReadMessageApiView.as_view(), name="message_read"),
    path("message/user/unread/", views.UserMessageAPIView.as_view(), name="message_user")
]
