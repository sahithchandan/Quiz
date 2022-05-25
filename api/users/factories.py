import factory.fuzzy

from api.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: "test_user_{}".format(n))

    class Meta:
        model = User
