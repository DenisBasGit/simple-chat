from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class ThreadUserRelation(models.Model):
    """Thread user relation model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="thread")
    thread = models.ForeignKey("chat.Thread", on_delete=models.CASCADE, related_name="user")

    class Meta:
        verbose_name = _("Thread User relation")
        verbose_name_plural = _("Thread User relations")
        unique_together = ("user", "thread")


class Thread(models.Model):
    """Thread model"""
    participants = models.ManyToManyField(to=User, through=ThreadUserRelation, related_name="threads")
    created = models.DateTimeField(auto_now_add=True, db_index=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Thread")
        verbose_name_plural = _("Threads")
