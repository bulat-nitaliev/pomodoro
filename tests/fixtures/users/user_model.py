from pytest_factoryboy import register
from faker import Factory as FakerFactory
import factory
from app.users.user_profile.models import UserProfile


EXISTS_GOOGLE_USER = "bulat@mail.ru"
EXISTS_GOOGLE_PASSWORD = "bulat"


faker = FakerFactory.create()

@register(name='user_profile')
class FakeUserProfile(factory.Factory):
    class Meta:
        model = UserProfile

    id = factory.LazyFunction(lambda: faker.random_int())
    username = factory.LazyFunction(lambda: faker.name())
    password = factory.LazyFunction(lambda: faker.password())