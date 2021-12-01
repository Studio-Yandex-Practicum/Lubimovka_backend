import factory
from faker import Faker

from apps.content_pages.models.content_items import (
    Preamble,
    Quote,
    Text,
    Title,
)

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
