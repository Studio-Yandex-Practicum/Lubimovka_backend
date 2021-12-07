import factory
import pytz
from django.contrib.contenttypes.models import ContentType
from faker import Faker

from apps.articles.models import BlogItem, BlogItemContent, BlogPerson
from apps.content_pages.models import Image
from apps.content_pages.tests.factories import (
    ImagesBlockFactory,
    PersonsBlockFactory,
    PlaysBlockFactory,
    PreambleFactory,
    QuoteFactory,
    TextFactory,
    TitleFactory,
)
from apps.core.decorators import restrict_factory
from apps.core.models import Person, Role
from apps.library.models.play import Play

fake = Faker(locale="ru_RU")


@restrict_factory({"global": [Person, Role]})
class BlogPersonFactory(factory.django.DjangoModelFactory):
    """
    Creates co-author for Blog.
    You should create at least one Person and Role
    before use this factory.
    """

    class Meta:
        model = BlogPerson

    person = factory.Iterator(Person.objects.all())
    role = factory.Iterator(Role.objects.all())


class BlogItemContentFactory(factory.django.DjangoModelFactory):
    """
    Base model for content items and blocks for Blog. When add content
    to Blog (via add_item_to_blog - see below) you should add
    item=factory.SubFactory(BLOCK_OR_ITEM_FACTORY_YOU_NEED), content_page=BLOG
    and count=INT.
    """

    class Meta:
        model = BlogItemContent

    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.item)
    )
    object_id = factory.SelfAttribute("item.id")
    order = factory.Sequence(lambda n: n)


def add_item_to_blog(blog, created, count, factory):
    """Add content item or block to Blog."""
    if not created:
        return
    if count:
        BlogItemContentFactory.create_batch(
            count, item=factory, content_page=blog
        )


@restrict_factory({"add_block_image": [Image], "add_block_play": [Play]})
class BlogFactory(factory.django.DjangoModelFactory):
    """
    Creates Blog Page.
    You can customize Blog's content by adding method and count when
    create (e.g. 'BlogFactory.create(add_preamble=5, add_block_person=3)).
    Content item/block will not be created if relevant method are not
    mentioned.
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
    is_draft = fake.boolean(chance_of_getting_true=25)
    pub_date = fake.date_time().replace(tzinfo=pytz.UTC)
    title = factory.Faker("text", locale="ru_RU", max_nb_chars=50)

    @factory.post_generation
    def add_co_author(self, created, count, **kwargs):
        """Add co-author for Blog."""
        if not created:
            return
        if count:
            BlogPersonFactory.create_batch(count, blog=self)

    @factory.post_generation
    def add_preamble(self, created, count, **kwargs):
        """Add Preamble item for Blog."""
        add_item_to_blog(
            self, created, count, factory.SubFactory(PreambleFactory)
        )

    @factory.post_generation
    def add_text(self, created, count, **kwargs):
        """Add Text item for Blog."""
        add_item_to_blog(self, created, count, factory.SubFactory(TextFactory))

    @factory.post_generation
    def add_title(self, created, count, **kwargs):
        """Add Title item for Blog."""
        add_item_to_blog(
            self, created, count, factory.SubFactory(TitleFactory)
        )

    @factory.post_generation
    def add_quote(self, created, count, **kwargs):
        """Add Quote item for Blog."""
        add_item_to_blog(
            self, created, count, factory.SubFactory(QuoteFactory)
        )

    @factory.post_generation
    def add_block_person(self, created, count, **kwargs):
        """Add content block with Persons."""
        add_item_to_blog(
            self, created, count, factory.SubFactory(PersonsBlockFactory)
        )

    @factory.post_generation
    def add_block_image(self, created, count, **kwargs):
        """Add content block with Images."""
        add_item_to_blog(
            self, created, count, factory.SubFactory(ImagesBlockFactory)
        )

    @factory.post_generation
    def add_block_play(self, created, count, **kwargs):
        """Add content block with Plays."""
        add_item_to_blog(
            self, created, count, factory.SubFactory(PlaysBlockFactory)
        )

    @classmethod
    def complex_create(cls):
        """Creates Blog with fully populated content."""
        return cls.create(
            add_co_author=1,
            add_preamble=1,
            add_text=1,
            add_title=1,
            add_quote=1,
            add_block_play=1,
            add_block_image=1,
            add_block_person=1,
        )
