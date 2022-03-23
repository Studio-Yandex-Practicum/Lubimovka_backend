import factory
from faker import Faker
from faker.providers.phone_number.ru_RU import Provider

from apps.library.models import UNIQUE_CONSTRAINT_FIELDS_FOR_PARTICIPATION, ParticipationApplicationFestival

fake = Faker("ru_RU")


class RussianPhoneNumberProvider(Provider):
    def custom_russian_phone_number(self):
        return f"+79{self.msisdn()[4:]}"


fake.add_provider(RussianPhoneNumberProvider)


class ParticipationApplicationFestivalFactory(factory.django.DjangoModelFactory):
    """Create ParticipationApplicationFestival object."""

    class Meta:
        model = ParticipationApplicationFestival
        django_get_or_create = UNIQUE_CONSTRAINT_FIELDS_FOR_PARTICIPATION

    first_name = factory.Faker("first_name", locale="ru_RU")
    last_name = factory.Faker("last_name", locale="ru_RU")
    birth_year = factory.Faker("year")
    city = factory.Faker("city_name", locale="ru_RU")
    phone_number = factory.LazyAttribute(lambda _: fake.custom_russian_phone_number())
    email = factory.Faker("email")
    title = factory.LazyFunction(lambda: fake.word().capitalize())
    year = factory.Faker("year")
    file = factory.LazyAttribute(lambda application: f"{application.title}.txt")
