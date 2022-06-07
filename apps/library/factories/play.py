import random
from typing import Iterable

import factory
from faker import Faker

from apps.core.constants import AUTHORS_COUNT, YOUTUBE_VIDEO_LINKS
from apps.core.decorators import restrict_factory
from apps.core.utils import slugify
from apps.info.models import Festival
from apps.library.models import Play, ProgramType
from apps.library.models.author import Author

fake = Faker("ru_RU")


class ProgramTypeFactory(factory.django.DjangoModelFactory):
    """Create ProgramType object."""

    class Meta:
        model = ProgramType
        django_get_or_create = ("name",)

    name = factory.Faker("text", max_nb_chars=50, locale="ru_RU")
    slug = factory.LazyAttribute(lambda program_type: slugify(program_type.name)[:40])


@restrict_factory(general=(Author, Festival, ProgramType))
class PlayFactory(factory.django.DjangoModelFactory):
    """Create Play object."""

    class Meta:
        model = Play
        django_get_or_create = ("name",)

    name = factory.Faker("text", max_nb_chars=60, locale="ru_RU")
    city = factory.Faker("city_name", locale="ru_RU")
    year = factory.Faker("random_int", min=1990, max=2021)
    url_download = factory.django.FileField(filename="example.pdf")
    published = factory.Faker("boolean", chance_of_getting_true=50)
    other_play = False
    url_reading = factory.Iterator(YOUTUBE_VIDEO_LINKS)

    @factory.lazy_attribute
    def program(self):
        return ProgramType.objects.order_by("?").first()

    @factory.lazy_attribute
    def festival(self):
        return Festival.objects.order_by("?").first()

    @factory.post_generation
    def authors(self, created: bool, extracted: Iterable[Author], **kwargs):
        """Add a Author(s) to play.

        To add concrete authors use
        PlayFactory.create(authors=(author1, author2, ...)).
        """
        if not created:
            return
        if extracted:
            authors = extracted
            self.authors.add(*authors)
            return

        how_many = random.choice(AUTHORS_COUNT)

        authors = Author.objects.order_by("?")[:how_many]
        self.authors.add(*authors)


class OtherPlayFactory(factory.django.DjangoModelFactory):
    """Create other Play object."""

    class Meta:
        model = Play
        django_get_or_create = ("name",)

    name = factory.Faker("text", max_nb_chars=60, locale="ru_RU")
    published = factory.Faker("boolean", chance_of_getting_true=50)
    url_download = factory.django.FileField()
    other_play = True
