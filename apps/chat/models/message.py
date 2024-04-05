from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from .threads import Thread

User = get_user_model()


class Message(models.Model):
    """Message model"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField(max_length=1000)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="messages")
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ["-created"]
