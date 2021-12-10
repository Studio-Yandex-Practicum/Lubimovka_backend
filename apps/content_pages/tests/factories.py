import factory

from apps.content_pages.models import (
    ContentPersonRole,
    ExtendedPerson,
    Image,
    ImagesBlock,
    OrderedImage,
    OrderedPlay,
    PersonsBlock,
    PlaysBlock,
    Preamble,
    Quote,
    Text,
    Title,
)
from apps.core.decorators import restrict_factory
from apps.core.models import Person, Role
from apps.library.models import Play


class ImageForContentFactory(factory.django.DjangoModelFactory):
    """Creates image for content block."""

    class Meta:
        model = Image
        django_get_or_create = ("image",)

    image = factory.django.ImageField(color=factory.Faker("color"))
    title = factory.Faker("sentence", locale="ru_RU")


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


@restrict_factory({"global": (Role,)})
class ContentPersonRoleFactory(factory.django.DjangoModelFactory):
    """
    Creates 'through' object with attrs ExtendedPerson and Role.
    For using in ExtendedPersonFactory.
    """

    class Meta:
        model = ContentPersonRole

    role = factory.Iterator(Role.objects.all())


@restrict_factory({"global": (Person,)})
class ExtendedPersonFactory(factory.django.DjangoModelFactory):
    """
    Create Person with order and role for block.
    You should create at least one Person and Role before
    using factory. Order in factory assume that there are not
    more than 3 ordered persons in a block.
    """

    class Meta:
        model = ExtendedPerson

    order = factory.Sequence(lambda n: (n % 3 + 1))
    person = factory.Iterator(Person.objects.all())

    @factory.post_generation
    def add_roles(self, created, extracted, **kwargs):
        """Add two roles to Person."""
        if not created:
            return
        ContentPersonRoleFactory.create_batch(2, extended_person=self)


class PersonsBlockFactory(factory.django.DjangoModelFactory):
    """
    Creates content block Person for blog, news or projects.
    Block creates with 3 ordered persons.
    """

    class Meta:
        model = PersonsBlock

    title = factory.Faker("text", locale="ru_RU", max_nb_chars=20)

    @factory.post_generation
    def add_person(self, created, extracted, **kwargs):
        if not created:
            return
        ExtendedPersonFactory.create_batch(3, block=self)


@restrict_factory({"global": (Image,)})
class OrderedImageFactory(factory.django.DjangoModelFactory):
    """
    Create Image with order for block. Order in factory assume
    that there are not more than 3 ordered images in a block.
    """

    class Meta:
        model = OrderedImage

    item = factory.Iterator(Image.objects.all())
    order = factory.Sequence(lambda n: (n % 3 + 1))


class ImagesBlockFactory(factory.django.DjangoModelFactory):
    """
    Creates content block Image for blog, news or projects.
    Block creates with 3 ordered images.
    """

    class Meta:
        model = ImagesBlock

    title = factory.Faker("text", locale="ru_RU", max_nb_chars=20)

    @factory.post_generation
    def add_image(self, created, extracted, **kwargs):
        if not created:
            return
        OrderedImageFactory.create_batch(3, block=self)


@restrict_factory({"global": (Play,)})
class OrderedPlayFactory(factory.django.DjangoModelFactory):
    """
    Creates Play with order for block. Order in factory assume
    that there are not more than 3 ordered person in a block.
    """

    class Meta:
        model = OrderedPlay

    item = factory.Iterator(Play.objects.all())
    order = factory.Sequence(lambda n: (n % 3 + 1))


class PlaysBlockFactory(factory.django.DjangoModelFactory):
    """
    Creates content block Play for blog, news or projects.
    Block creates with 3 ordered plays.
    """

    class Meta:
        model = PlaysBlock

    title = factory.Faker("text", locale="ru_RU", max_nb_chars=20)

    @factory.post_generation
    def add_play(self, created, extracted, **kwargs):
        if not created:
            return
        OrderedPlayFactory.create_batch(3, block=self)
