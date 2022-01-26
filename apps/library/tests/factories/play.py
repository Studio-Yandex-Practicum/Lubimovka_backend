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
        django_get_or_create = ["name"]

    name = factory.LazyFunction(lambda: fake["ru_RU"].word().capitalize())
    slug = factory.Faker("word", locale="en_US")


@restrict_factory({"global": [Festival, ProgramType]})
class PlayFactory(factory.django.DjangoModelFactory):
    """
    Create Play object.

    You should create at least one Festival and Program
    before use this factory.
    """

    class Meta:
        model = Play
        django_get_or_create = ["name"]

    name = factory.LazyFunction(lambda: fake.word().capitalize())
    city = factory.Faker("city_name", locale="ru_RU")
    year = factory.Faker("random_int", min=1990, max=2021, step=1)
    url_download = factory.LazyAttribute(lambda obj: f"www.plays-download/{obj.name}")
    url_reading = factory.LazyAttribute(lambda obj: f"www.plays-reading/{obj.name}")
    program = factory.Iterator(ProgramType.objects.all())
    festival = factory.Iterator(Festival.objects.all())
    is_draft = factory.Faker("boolean", chance_of_getting_true=25)
