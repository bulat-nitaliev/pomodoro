import factory
from faker import Factory as FakerFactory
from pytest_factoryboy import register
from app.tasks.models import Tasks, Category


faker = FakerFactory.create()


@register(name="tasks")
class FakeTasks(factory.Factory):
    class Meta:
        model = Tasks

    id = factory.LazyFunction(lambda: faker.random_int())
    name = factory.LazyFunction(lambda: faker.name())
    pomodoro_count = factory.LazyFunction(lambda: faker.random_int())
    category_id = factory.LazyFunction(lambda: faker.random_int())
    user_id = factory.LazyFunction(lambda: faker.random_int())


@register(name="category")
class FakeCategory(factory.Factory):
    class Meta:
        model = Category

    id = factory.LazyFunction(lambda: faker.random_int())
    name = factory.LazyFunction(lambda: faker.name())
    type = factory.LazyFunction(lambda: faker.name())
