import factory
from django.contrib.contenttypes.models import ContentType
from faker import Faker

from apps.articles.models import BlogItem, BlogItemContent, BlogPerson
from apps.content_pages.tests.factories import (
    ImagesBlockFactory,
    OrderedImageFactory,
    OrderedPersonFactory,
    OrderedPlayFactory,
    PersonsBlockFactory,
    PlaysBlockFactory,
    PreambleFactory,
    QuoteFactory,
    TextFactory,
    TitleFactory,
)
from apps.core.tests.factories import PersonFactory, RoleFactory

fake = Faker(locale="ru_RU")


class BlogPersonFactory(factory.django.DjangoModelFactory):
    """Creates co-author for Blog."""

    class Meta:
        model = BlogPerson

    person = factory.SubFactory(PersonFactory)
    role = factory.SubFactory(RoleFactory)


class ItemContentFactory(factory.django.DjangoModelFactory):
    """Base factory model for blocks."""

    object_id = factory.SelfAttribute("item.id")
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.item)
    )

    class Meta:
        exclude = ("item",)
        abstract = True


class ImageContentFactory(ItemContentFactory):
    """Creates empty block with Images content."""

    item = factory.SubFactory(ImagesBlockFactory)
    order = 5

    class Meta:
        model = BlogItemContent


class PersonContentFactory(ItemContentFactory):
    """Creates empty block with Persons content."""

    item = factory.SubFactory(PersonsBlockFactory)
    order = 4

    class Meta:
        model = BlogItemContent


class PlayContentFactory(ItemContentFactory):
    """Creates empty block with Plays content."""

    item = factory.SubFactory(PlaysBlockFactory)
    order = 6

    class Meta:
        model = BlogItemContent


class PreambleContentFactory(ItemContentFactory):
    """Creates item Preamble."""

    item = factory.SubFactory(PreambleFactory)

    class Meta:
        model = BlogItemContent


class TextContentFactory(ItemContentFactory):
    item = factory.SubFactory(TextFactory)

    class Meta:
        model = BlogItemContent


class TitleContentFactory(ItemContentFactory):
    item = factory.SubFactory(TitleFactory)

    class Meta:
        model = BlogItemContent


class QuoteContentFactory(ItemContentFactory):
    item = factory.SubFactory(QuoteFactory)

    class Meta:
        model = BlogItemContent


class PageFactory(factory.django.DjangoModelFactory):
    """Abstract Factory for Page."""

    title = factory.Faker("text", locale="ru_RU", max_nb_chars=50)
    description = factory.Faker(
        "paragraph",
        locale="ru_RU",
        nb_sentences=5,
        variable_nb_sentences=False,
    )
    content = factory.RelatedFactory(PreambleContentFactory, "content_page")
    content1 = factory.RelatedFactory(TextContentFactory, "content_page")
    content2 = factory.RelatedFactory(TitleContentFactory, "content_page")
    content3 = factory.RelatedFactory(QuoteContentFactory, "content_page")
    content4 = factory.RelatedFactory(PersonContentFactory, "content_page")
    content5 = factory.RelatedFactory(ImageContentFactory, "content_page")
    content6 = factory.RelatedFactory(PlayContentFactory, "content_page")

    @factory.post_generation
    def add_person_to_block(self, created, extracted, **kwargs):
        if not created:
            return
        if extracted:
            person_block = self.contents.get(order=4)
            for index in range(3):
                ordered_person = OrderedPersonFactory.create(
                    block=person_block.item, order=index
                )
                person = ordered_person.item
                person_block.item.items.add(person)

    @factory.post_generation
    def add_image_to_block(self, created, extracted, **kwargs):
        if not created:
            return
        if extracted:
            image_block = self.contents.get(order=5)
            for index in range(3):
                ordered_image = OrderedImageFactory.create(
                    block=image_block.item, order=index
                )
                image = ordered_image.item
                image_block.item.items.add(image)

    @factory.post_generation
    def add_plays_to_block(self, created, extracted, **kwargs):
        """Add Plays to Block."""
        if not created:
            return
        if extracted:
            play_block = self.contents.get(order=6)
            for index in range(3):
                ordered_play = OrderedPlayFactory.create(
                    block=play_block.item, order=index
                )
                play = ordered_play.item
                play_block.item.items.add(play)

    @classmethod
    def complex_create(cls):
        """Create Blog object with fully populated fields."""
        return cls.create(
            add_person_to_block=True,
            add_image_to_block=True,
            add_plays_to_block=True,
        )


class BlogFactory(PageFactory):
    """Creates BlogPage with content."""

    class Meta:
        model = BlogItem

    co_author = factory.RelatedFactory(BlogPersonFactory, "blog")
    author_url_title = factory.Faker("name", locale="ru_RU")
    author_url = factory.Faker("url")
