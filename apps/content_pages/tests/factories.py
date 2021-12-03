import factory
from faker import Faker

from apps.content_pages.models.content_blocks import (
    ImagesBlock,
    OrderedImage,
    OrderedPerson,
    OrderedPlay,
    PersonsBlock,
    PlaysBlock,
)
from apps.content_pages.models.content_items import (
    Preamble,
    Quote,
    Text,
    Title,
)
from apps.core.tests.factories import ImageFactory, PersonFactory
from apps.library.tests.factories import PlayFactory

fake = Faker(locale="ru_RU")


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

    item = factory.SubFactory(ImageFactory)
    block = factory.SubFactory(ImagesBlockFactory)
    order = factory.Sequence(lambda n: n)


class PlayBlockFactory(factory.django.DjangoModelFactory):
    """Creates content block Play for blog, news or projects."""

    class Meta:
        model = PlaysBlock

    title = factory.Faker("text", locale="ru_RU", max_nb_chars=20)


class OrderedPlayFactory(factory.django.DjangoModelFactory):
    """Creates Play with order for block."""

    class Meta:
        model = OrderedPlay

    item = factory.SubFactory(PlayFactory)
    block = factory.SubFactory(PlayBlockFactory)
    order = factory.Sequence(lambda n: n)
