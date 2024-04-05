from typing import TYPE_CHECKING, Any, Dict

from apps.chat.models import Message

if TYPE_CHECKING:
    from django.contrib.auth.models import User


class MessageService:
    """Message service"""

    @classmethod
    def _create(cls, data: Dict[str, Any]) -> Message:
        """
        Main create message
        Args:
            data: Dict[str, Any]
        Return:
            message: Message
        """
        return Message.objects.create(**data)

    @classmethod
    def create(cls, data: Dict[str, Any]) -> Message:
        """
        Create message
        Args:
            data: Dict[str, Any]
        Return:
            message: Message
        """
        return cls._create(data)

    @classmethod
    def read(cls, message: Message) -> None:
        """
        Read message
        Args:
            message: Message
        """
        message.is_read = True
        message.save(update_fields=["is_read"])

    @classmethod
    def is_user_sender(cls, obj: Message, user: "User") -> bool:
        """
        Check if user is sender

        Args:
            obj: Message
            user: User
        Return: bool
        """
        return obj.sender == user
