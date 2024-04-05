from rest_framework import serializers

from apps.chat.models.message import Message
from apps.chat.models.threads import Thread, User
from apps.chat.services import ThreadService
from apps.chat.services.message import MessageService


class CreateThreadSerializer(serializers.Serializer):
    """Create thread serializer"""

    id = serializers.IntegerField(read_only=True)
    participant = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, required=True)
    created = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """Create method"""
        instance, self.created = ThreadService.create(**validated_data)
        return instance


class ThreadSerializer(serializers.ModelSerializer):
    """Thread Serializer"""

    class Meta:
        model = Thread
        fields = "__all__"


class CreateMessageSerializer(serializers.ModelSerializer):
    """Create Message serializer"""
    class Meta:
        """Metaclass for CreateMessageSerializer"""
        model = Message
        fields = ["text"]

    def create(self, validated_data):
        """Create method"""
        return MessageService.create(validated_data)


class MessageSerializer(serializers.ModelSerializer):
    """Message Serializer"""

    sender = serializers.SerializerMethodField()

    class Meta:
        """Metaclass for MessageSerializer"""
        model = Message
        fields = ["id", "sender", "text", "created", "is_read"]

    @staticmethod
    def get_sender(obj: Message) -> str:
        """
        Get sender method

        Get first and last name of sender from message
        Return:
            full_name(str)
        """
        return "%s %s" % (obj.sender.first_name, obj.sender.last_name)
