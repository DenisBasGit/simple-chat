import factory

from apps.chat.models import Thread
from tests.users.factory import UserFactory


class ThreadFactory(factory.django.DjangoModelFactory):
    """Thread Factory"""

    class Meta:
        model = Thread

    @factory.post_generation
    def participants(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            tags = extracted
        else:
            tags = [UserFactory() for x in range(2)]
        for tag in tags:
            self.participants.add(tag)
