import factory
from django.contrib.contenttypes.models import ContentType
from faker import Faker

from apps.articles.models import BlogItem, BlogItemContent
from apps.content_pages.tests.factories import (
    PersonsBlockFactory,
    PreambleFactory,
    QuoteFactory,
    TextFactory,
    TitleFactory,
)
from apps.core.tests.factories import PersonFactory

fake = Faker(locale="ru_RU")


class BlogItemContentFactory(factory.django.DjangoModelFactory):
    object_id = factory.SelfAttribute("item.id")
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.item)
    )

    class Meta:
        exclude = ("item",)
        abstract = True


class BlogPersonBlockContentFactory(BlogItemContentFactory):
    item = factory.SubFactory(PersonsBlockFactory)
    order = 4

    class Meta:
        model = BlogItemContent


class BlogPreambleContentFactory(BlogItemContentFactory):
    item = factory.SubFactory(PreambleFactory)

    class Meta:
        model = BlogItemContent


class BlogTextContentFactory(BlogItemContentFactory):
    item = factory.SubFactory(TextFactory)

    class Meta:
        model = BlogItemContent


class BlogTitleContentFactory(BlogItemContentFactory):
    item = factory.SubFactory(TitleFactory)

    class Meta:
        model = BlogItemContent


class BlogQuoteContentFactory(BlogItemContentFactory):
    item = factory.SubFactory(QuoteFactory)

    class Meta:
        model = BlogItemContent


class BlogFactory(factory.django.DjangoModelFactory):
    """Creates BlogPage with content."""

    class Meta:
        model = BlogItem

    title = factory.Faker("text", locale="ru_RU", max_nb_chars=50)
    description = factory.Faker(
        "paragraph",
        locale="ru_RU",
        nb_sentences=5,
        variable_nb_sentences=False,
    )
    author_url_title = factory.Faker("name", locale="ru_RU")
    author_url = factory.Faker("url")
    content = factory.RelatedFactory(
        BlogPreambleContentFactory, "content_page"
    )
    content1 = factory.RelatedFactory(BlogTextContentFactory, "content_page")
    content2 = factory.RelatedFactory(BlogTitleContentFactory, "content_page")
    content3 = factory.RelatedFactory(BlogQuoteContentFactory, "content_page")
    content4 = factory.RelatedFactory(
        BlogPersonBlockContentFactory, "content_page"
    )

    @factory.post_generation
    def add_person_to_block(self, created, extracted, **kwargs):
        if not created:
            return
        if extracted:
            person_block = self.contents.get(order=4)
            for _ in range(3):
                person = PersonFactory.create()
                person_block.item.items.add(person)
