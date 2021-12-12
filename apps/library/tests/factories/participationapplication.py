import factory
import pytz
from faker import Faker

from apps.library.models import ParticipationApplicationFestival

fake = Faker("ru_RU")


class ParticipationApplicationFestivalFactory(
    factory.django.DjangoModelFactory
):
    """
    Create ParticipationApplicationFestival object.
    """

    class Meta:
        model = ParticipationApplicationFestival

    first_name = factory.Faker("first_name", locale="ru_RU")
    last_name = factory.Faker("last_name", locale="ru_RU")
    birthday = factory.LazyFunction(
        lambda: fake.past_datetime(tzinfo=pytz.UTC)
    )
    city = factory.Faker("city_name", locale="ru_RU")
    phone_number = factory.Faker("phone_number")
    email = factory.Faker("email")
    title = factory.LazyFunction(lambda: fake.word().capitalize())
    year = factory.Faker("year")
    file = factory.LazyAttribute(lambda obj: f"{obj.title}.txt")
