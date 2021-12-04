import random

import factory
from faker import Faker

from apps.content_pages.models import (
    Image,
    ImagesBlock,
    OrderedImage,
    OrderedPerson,
    OrderedPlay,
    PersonsBlock,
    PlaysBlock,
    Preamble,
    Quote,
    Text,
    Title,
)
from apps.core.tests.factories import PersonFactory
from apps.library.tests.factories import PlayFactory

fake = Faker(locale="ru_RU")


class ImageConFactory(factory.django.DjangoModelFactory):
    """Creates image for content block."""

    class Meta:
        model = Image
        django_get_or_create = ("image",)

    image = factory.django.ImageField(
        color=factory.LazyFunction(
            lambda: random.choice(["blue", "yellow", "green", "orange"])
        ),
        width=factory.LazyFunction(lambda: random.randint(10, 1000)),
        height=factory.SelfAttribute("width"),
    )
    title = factory.Faker("text", locale="ru_RU", max_nb_chars=20)


class PreambleFactory(factory.django.DjangoModelFactory):
    """Creates content item Preamble for blog, news or projects."""

    class Meta:
        model = Preamble

    preamble = factory.Faker("text", locale="ru_RU")


class TextFactory(factory.django.DjangoModelFactory):
    """Creates content item Text for blog, news or projects."""

    class Meta:
        model = Text

    text = factory.Faker(
        "paragraph",
        locale="ru_RU",
        nb_sentences=5,
        variable_nb_sentences=False,
    )


class TitleFactory(factory.django.DjangoModelFactory):
    """Creates content item Title for blog, news or projects."""

    class Meta:
        model = Title

    title = factory.Faker("text", locale="ru_RU", max_nb_chars=20)


class QuoteFactory(factory.django.DjangoModelFactory):
    """Creates content item Quote for blog, news or projects."""

    class Meta:
        model = Quote

    quote = factory.Faker("text", locale="ru_RU")


class PersonsBlockFactory(factory.django.DjangoModelFactory):
    """Creates content block Person for blog, news or projects."""

    class Meta:
        model = PersonsBlock

    title = factory.Faker("text", locale="ru_RU", max_nb_chars=20)


class OrderedPersonFactory(factory.django.DjangoModelFactory):
    """Create Person with order for block."""

    class Meta:
        model = OrderedPerson

    item = factory.SubFactory(PersonFactory)
    block = factory.SubFactory(PersonsBlockFactory)
    order = factory.Sequence(lambda n: n)


class ImagesBlockFactory(factory.django.DjangoModelFactory):
    """Creates content block Image for blog, news or projects."""

    class Meta:
        model = ImagesBlock

    title = factory.Faker("text", locale="ru_RU", max_nb_chars=20)


class OrderedImageFactory(factory.django.DjangoModelFactory):
    """Create Image with order for block."""

    class Meta:
        model = OrderedImage

    item = factory.SubFactory(ImageConFactory)
    block = factory.SubFactory(ImagesBlockFactory)
    order = factory.Sequence(lambda n: n)


class PlaysBlockFactory(factory.django.DjangoModelFactory):
    """Creates content block Play for blog, news or projects."""

    class Meta:
        model = PlaysBlock

    title = factory.Faker("text", locale="ru_RU", max_nb_chars=20)


class OrderedPlayFactory(factory.django.DjangoModelFactory):
    """Creates Play with order for block."""

    class Meta:
        model = OrderedPlay

    item = factory.SubFactory(PlayFactory)
    block = factory.SubFactory(PlaysBlockFactory)
    order = factory.Sequence(lambda n: n)
