from rest_framework.permissions import BasePermission

from apps.chat.services import ThreadService
from apps.chat.services.message import MessageService


class IsParticipantOfThreadPermission(BasePermission):
    """Check if user is participant of thread"""

    def has_object_permission(self, request, view, obj) -> bool:
        """Has object permission"""
        return ThreadService.is_participant_of_thread(obj, request.user)


class IsMessageOfTheadPermission(BasePermission):
    """Check if a message related to thread"""

    def has_object_permission(self, request, view, obj) -> bool:
        """Has object permission"""
        return ThreadService.is_participant_of_thread(obj.thread, request.user)


class IsMessageCannotReadPermission(BasePermission):
    """Chechk if request user not a sender"""

    message = "You cannot mark as read your own message"

    def has_object_permission(self, request, view, obj) -> bool:
        """Has object permission"""
        return not MessageService.is_user_sender(obj, request.user)
