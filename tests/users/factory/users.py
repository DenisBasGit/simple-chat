import factory
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for User"""

    email = factory.faker.Faker("email")
    username = factory.Sequence(lambda n: "username%s" % n)

    class Meta:
        model = User
