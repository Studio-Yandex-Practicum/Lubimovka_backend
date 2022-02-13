import factory
from faker import Faker

from apps.core.decorators import restrict_factory
from apps.info.models import Festival
from apps.library.models import Play, ProgramType

fake = Faker("ru_RU")


class ProgramFactory(factory.django.DjangoModelFactory):
    """Create ProgramType object."""

    class Meta:
        model = ProgramType
        django_get_or_create = ("name",)

    name = factory.LazyFunction(lambda: fake["ru_RU"].word().capitalize())
    slug = factory.Faker("word", locale="en_US")


@restrict_factory({"global": (Festival, ProgramType)})
class PlayFactory(factory.django.DjangoModelFactory):
    """Create Play object."""

    class Meta:
        model = Play
        django_get_or_create = ("name",)

    name = factory.LazyFunction(lambda: fake.word().capitalize())
    city = factory.Faker("city_name", locale="ru_RU")
    year = factory.Faker("random_int", min=1990, max=2021)
    url_download = factory.django.FileField()
    url_reading = factory.LazyAttribute(lambda play: f"www.plays-reading/{play.name}")
    is_draft = factory.Faker("boolean", chance_of_getting_true=25)

    @factory.lazy_attribute
    def program(self):
        return ProgramType.objects.order_by("?").first()

    @factory.lazy_attribute
    def festival(self):
        return Festival.objects.order_by("?").first()
