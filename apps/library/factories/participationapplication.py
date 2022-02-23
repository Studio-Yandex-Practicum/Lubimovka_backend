import factory
from faker import Faker

from apps.library.models import UNIQUE_CONSTRAINT_FIELDS_FOR_PARTICIPATION, ParticipationApplicationFestival

fake = Faker("ru_RU")


class ParticipationApplicationFestivalFactory(factory.django.DjangoModelFactory):
    """Create ParticipationApplicationFestival object."""

    class Meta:
        model = ParticipationApplicationFestival
        django_get_or_create = UNIQUE_CONSTRAINT_FIELDS_FOR_PARTICIPATION

    first_name = factory.Faker("first_name", locale="ru_RU")
    last_name = factory.Faker("last_name", locale="ru_RU")
    birth_year = factory.Faker("year")
    city = factory.Faker("city_name", locale="ru_RU")
    phone_number = factory.Faker("phone_number")
    email = factory.Faker("email")
    title = factory.LazyFunction(lambda: fake.word().capitalize())
    year = factory.Faker("year")
    file = factory.LazyAttribute(lambda application: f"{application.title}.txt")
