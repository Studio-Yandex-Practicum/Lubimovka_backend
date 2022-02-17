import factory

from apps.content_pages.models import Link, Preamble, Quote, Text, Title


class LinkFactory(factory.django.DjangoModelFactory):
    """Create content item Link for project."""

    class Meta:
        model = Link

    description = factory.Faker(
        "paragraph",
        locale="ru_RU",
        nb_sentences=5,
        variable_nb_sentences=False,
    )
    title = factory.Faker("sentence", locale="ru_RU")
    url = factory.Faker("url")


class PreambleFactory(factory.django.DjangoModelFactory):
    """Create content item Preamble for blog, news or projects."""

    class Meta:
        model = Preamble

    preamble = factory.Faker("text", locale="ru_RU")


class QuoteFactory(factory.django.DjangoModelFactory):
    """Create content item Quote for blog, news or projects."""

    class Meta:
        model = Quote

    quote = factory.Faker("text", locale="ru_RU")


class TextFactory(factory.django.DjangoModelFactory):
    """Create content item Text for blog, news or projects."""

    class Meta:
        model = Text

    text = factory.Faker(
        "paragraph",
        locale="ru_RU",
        nb_sentences=5,
        variable_nb_sentences=False,
    )


class TitleFactory(factory.django.DjangoModelFactory):
    """Create content item Title for blog, news or projects."""

    class Meta:
        model = Title

    title = factory.Faker("text", locale="ru_RU", max_nb_chars=20)
