from django.contrib import admin

from apps.chat.models import Message, Thread, ThreadUserRelation


class ThreadInline(admin.TabularInline):  # type: ignore
    """Thread inline admin class"""

    model = ThreadUserRelation
    extra = 1


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):  # type: ignore
    """Theread Admin"""

    inlines = [ThreadInline]
    list_filter = ["created"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):  # type: ignore
    """Message Admin"""

    list_display = ["sender", "thread", "created", "is_read"]
    list_filter = ["created", "is_read"]
