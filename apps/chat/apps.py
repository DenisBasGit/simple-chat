from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ChatConfig(AppConfig):
    """Chat config"""
    name = "apps.chat"
    verbose_name = _("Chat")
    default_auto_field = "django.db.models.BigAutoField"
