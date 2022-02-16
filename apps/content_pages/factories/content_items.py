import factory

from ..models import Image, Link, Preamble, Quote, Text, Title, Video


class ImageForContentFactory(factory.django.DjangoModelFactory):
    """Creates image for content block."""

    class Meta:
        model = Image
        django_get_or_create = ("image",)

    image = factory.django.ImageField(color=factory.Faker("color"))
    title = factory.Faker("sentence", locale="ru_RU")


class LinkFactory(factory.django.DjangoModelFactory):
    """Creates content item Link for project."""

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
    """Creates content item Preamble for blog, news or projects."""

    class Meta:
        model = Preamble

    preamble = factory.Faker("text", locale="ru_RU")


class QuoteFactory(factory.django.DjangoModelFactory):
    """Create content item Quote for blog, news or projects."""

    class Meta:
        model = Quote

    quote = factory.Faker("text", locale="ru_RU")


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


class VideoFactory(factory.django.DjangoModelFactory):
    """Create `content item` for videos block."""

    class Meta:
        model = Video

    description = factory.Faker(
        "paragraph",
        locale="ru_RU",
        nb_sentences=5,
        variable_nb_sentences=False,
    )
    title = factory.Faker("sentence", locale="ru_RU")
    url = factory.Faker("url")
