import random
from zoneinfo import ZoneInfo

import factory
from django.conf import settings

from apps.articles.models import BlogItem, BlogItemContent, BlogPerson
from apps.content_pages.factories import AbstractContentFactory
from apps.core.decorators.factory import restrict_factory
from apps.core.models import Person, Role
from apps.core.status_source import Status
from apps.library.models import Play


@restrict_factory(general=(BlogItem,))
class BlogItemContentModuleFactory(AbstractContentFactory):
    """ContentModule factory for `BlogItem`.

    1. Set relation to `BlogItem` object.
    2. The factory inherits generic relations to `ContentUnit` and `ContentArray`
    objects form `AbstractContentFactory`.
    """

    class Meta:
        model = BlogItemContent

    @factory.lazy_attribute
    def content_page(self):
        return BlogItem.objects.order_by("?").first()


@restrict_factory(general=(Person, Role, BlogItem))
class BlogPersonFactory(factory.django.DjangoModelFactory):
    """Create co-author for `BlogItem`."""

    class Meta:
        model = BlogPerson

    @factory.lazy_attribute
    def person(self):
        return Person.objects.order_by("?").first()

    @factory.lazy_attribute
    def role(self):
        return Role.objects.filter(types__role_type="blog_persons_role").order_by("?").first()

    @factory.lazy_attribute
    def blog(self):
        return BlogItem.objects.filter("?").first()


@restrict_factory(
    add_several_playsblock=(Play,),
    add_several_personsblock=(Person,),
)
class BlogItemFactory(factory.django.DjangoModelFactory):
    """Create `BlogItem` Page.

    You can customize Blog's content by adding method and count when
    create (e.g. 'BlogFactory.create(add_several_preamble=5,
    add_several_personsblock=3)). Content item/block will not be
    created if relevant method are not mentioned.
    You can use 'complex_create' which will create all content item/block
    each in single copy.
    Co-author can be added the same way.
    """

    class Meta:
        model = BlogItem

    author_url = factory.Faker("url")
    author_url_title = factory.Faker("name", locale="ru_RU")
    description = factory.Faker(
        "paragraph",
        locale="ru_RU",
        nb_sentences=5,
        variable_nb_sentences=False,
    )
    image = factory.django.ImageField(color=factory.Faker("color"))
    pub_date = factory.Faker("date_time", tzinfo=ZoneInfo(settings.TIME_ZONE))
    title = factory.Faker("text", locale="ru_RU", max_nb_chars=50)
    status = factory.LazyFunction(lambda: random.choice(list(Status)))

    @factory.post_generation
    def add_several_co_author(self, created, count, **kwargs):
        """Add specified count of co-authors to Blog."""
        if created and count:
            BlogPersonFactory.create_batch(count, blog=self)

    @factory.post_generation
    def add_several_imagesblock(self, created, count, **kwargs):
        """Add specified count of content block with Images to Blog."""
        if created and count:
            BlogItemContentModuleFactory.create_batch(count, content_page=self, array_image=True)

    @factory.post_generation
    def add_several_personsblock(self, created, count, **kwargs):
        """Add specified count of content block with Persons to Blog."""
        if created and count:
            BlogItemContentModuleFactory.create_batch(count, content_page=self, array_person=True)

    @factory.post_generation
    def add_several_playsblock(self, created, count, **kwargs):
        """Add specified count of content block with Plays to Blog."""
        if created and count:
            BlogItemContentModuleFactory.create_batch(count, content_page=self, array_play=True)

    @factory.post_generation
    def add_several_preamble(self, created, count, **kwargs):
        """Add specified count of Preamble item to Blog."""
        if created and count:
            BlogItemContentModuleFactory.create_batch(count, content_page=self, unit_preamble=True)

    @factory.post_generation
    def add_several_quote(self, created, count, **kwargs):
        """Add specified count of Quote item to Blog."""
        if created and count:
            BlogItemContentModuleFactory.create_batch(count, content_page=self, unit_quote=True)

    @factory.post_generation
    def add_several_text(self, created, count, **kwargs):
        """Add specified count of Text item to Blog."""
        if created and count:
            BlogItemContentModuleFactory.create_batch(count, content_page=self, unit_text=True)

    @factory.post_generation
    def add_several_title(self, created, count, **kwargs):
        """Add specified count of Title item to Blog."""
        if created and count:
            BlogItemContentModuleFactory.create_batch(count, content_page=self, unit_title=True)

    @classmethod
    def complex_create(cls, count):
        """Create specified count of Blog with fully populated content."""
        return cls.create_batch(
            count,
            add_several_co_author=1,
            add_several_preamble=1,
            add_several_text=1,
            add_several_title=1,
            add_several_quote=1,
            add_several_playsblock=1,
            add_several_imagesblock=1,
            add_several_personsblock=1,
        )
