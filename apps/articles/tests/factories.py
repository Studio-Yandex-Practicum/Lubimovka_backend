import random

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
from apps.core.models import Person, Role

fake = Faker(locale="ru_RU")


class BlogPersonFactory(factory.django.DjangoModelFactory):
    """Creates co-author for Blog."""

    class Meta:
        model = BlogPerson

    person = factory.Iterator(Person.objects.all())
    role = factory.Iterator(Role.objects.all())


class ItemContentFactory(factory.django.DjangoModelFactory):
    """Base model for blocks."""

    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.item)
    )
    object_id = factory.SelfAttribute("item.id")
    order = factory.Sequence(lambda n: n)

    class Meta:
        exclude = ("item",)
        abstract = True


class ImageContentFactory(ItemContentFactory):
    """Creates empty block with Images content."""

    item = factory.SubFactory(ImagesBlockFactory)

    class Meta:
        model = BlogItemContent


class PersonContentFactory(ItemContentFactory):
    """Creates empty block with Persons content."""

    item = factory.SubFactory(PersonsBlockFactory)

    class Meta:
        model = BlogItemContent


class PlayContentFactory(ItemContentFactory):
    """Creates empty block with Plays content."""

    item = factory.SubFactory(PlaysBlockFactory)

    class Meta:
        model = BlogItemContent


class PreambleContentFactory(ItemContentFactory):
    """Creates content item Preamble."""

    item = factory.SubFactory(PreambleFactory)

    class Meta:
        model = BlogItemContent


class TextContentFactory(ItemContentFactory):
    """Creates content item Text."""

    item = factory.SubFactory(TextFactory)

    class Meta:
        model = BlogItemContent


class TitleContentFactory(ItemContentFactory):
    """Creates content item Title."""

    item = factory.SubFactory(TitleFactory)

    class Meta:
        model = BlogItemContent


class QuoteContentFactory(ItemContentFactory):
    """Creates content item Quote."""

    item = factory.SubFactory(QuoteFactory)

    class Meta:
        model = BlogItemContent


class BlogFactory(factory.django.DjangoModelFactory):
    """Creates Blog Page."""

    class Meta:
        model = BlogItem

    author_url = factory.Faker("url")
    author_url_title = factory.Faker("name", locale="ru_RU")
    co_author = factory.RelatedFactory(BlogPersonFactory, "blog")
    description = factory.Faker(
        "paragraph",
        locale="ru_RU",
        nb_sentences=5,
        variable_nb_sentences=False,
    )
    is_draft = factory.LazyFunction(lambda: random.choice([True, False]))
    pub_date = factory.Faker("date_time")
    title = factory.Faker("text", locale="ru_RU", max_nb_chars=50)

    @factory.post_generation
    def add_content_items(self, created, extracted, **kwargs):
        """Add content items for Blog."""
        if not created:
            return
        if extracted:
            PreambleContentFactory.create(content_page=self)
            TextContentFactory.create(content_page=self)
            TitleContentFactory.create(content_page=self)
            QuoteContentFactory.create(content_page=self)

    @factory.post_generation
    def add_block_person(self, created, extracted, **kwargs):
        """Add content block with Persons."""
        if not created:
            return
        if extracted:
            person_block = PersonContentFactory.create(content_page=self)
            for index in range(3):
                ordered_person = OrderedPersonFactory.create(
                    block=person_block.item, order=index
                )
                person = ordered_person.item
                person_block.item.items.add(person)

    @factory.post_generation
    def add_block_image(self, created, extracted, **kwargs):
        """Add content block with Images."""
        if not created:
            return
        if extracted:
            image_block = ImageContentFactory.create(content_page=self)
            for index in range(3):
                ordered_image = OrderedImageFactory.create(
                    block=image_block.item, order=index
                )
                image = ordered_image.item
                image_block.item.items.add(image)

    @factory.post_generation
    def add_block_play(self, created, extracted, **kwargs):
        """Add content block with Plays."""
        if not created:
            return
        if extracted:
            play_block = PlayContentFactory.create(content_page=self)
            for index in range(3):
                ordered_play = OrderedPlayFactory.create(
                    block=play_block.item, order=index
                )
                play = ordered_play.item
                play_block.item.items.add(play)

    @classmethod
    def complex_create(cls):
        """Creates Blog with fully populated content."""
        return cls.create(
            add_content_items=True,
            add_block_play=True,
            add_block_image=True,
            add_block_person=True,
        )
