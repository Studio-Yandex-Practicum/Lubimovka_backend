import random

import factory
from faker import Faker

from apps.core.decorators import restrict_factory
from apps.core.utils import slugify
from apps.info.models import Festival
from apps.library.models import Play, ProgramType

fake = Faker("ru_RU")


class ProgramTypeFactory(factory.django.DjangoModelFactory):
    """Create ProgramType object."""

    class Meta:
        model = ProgramType
        django_get_or_create = ("name",)

    name = factory.Faker("text", max_nb_chars=50, locale="ru_RU")
    slug = factory.LazyAttribute(lambda program_type: slugify(program_type.name)[:40])


@restrict_factory(general=(Festival, ProgramType))
class PlayFactory(factory.django.DjangoModelFactory):
    """Create Play object."""

    class Meta:
        model = Play
        django_get_or_create = ("name",)

    name = factory.Faker("text", max_nb_chars=60, locale="ru_RU")
    city = factory.Faker("city_name", locale="ru_RU")
    year = factory.Faker("random_int", min=1990, max=2021)
    url_download = factory.django.FileField()
    url_reading = factory.LazyAttribute(lambda play: f"www.plays-reading/{play.name}")
    status = factory.LazyFunction(lambda: random.choice(list(Play.SelectPlayStatus)))

    @factory.lazy_attribute
    def program(self):
        return ProgramType.objects.order_by("?").first()

    @factory.lazy_attribute
    def festival(self):
        return Festival.objects.order_by("?").first()
