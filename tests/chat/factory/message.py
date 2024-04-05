import factory

from apps.chat.models import Message
from tests.users.factory import UserFactory

from .thread import ThreadFactory


class MessageFactory(factory.django.DjangoModelFactory):
    """Message factory"""
    sender = factory.SubFactory(UserFactory)
    text = factory.Faker('sentence')
    thread = factory.SubFactory(ThreadFactory)

    class Meta:
        model = Message
