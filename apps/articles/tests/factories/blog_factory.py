import factory
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

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


def add_content_item_to_blog(blog, created, count, factory):
    """Add specified count of content item or block to Blog."""
    if not created:
        return
    if count:
        BlogItemContentFactory.create_batch(count, item=factory, content_page=blog)


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
    role = factory.Iterator(Role.objects.filter(types__role_type="blog_persons_role"))


class BlogItemContentFactory(factory.django.DjangoModelFactory):
    """
    Base model for content items and blocks for Blog.

    When add content to Blog (via add_content_item_to_blog - see above) you should add
    item=factory.SubFactory(BLOCK_OR_ITEM_FACTORY_YOU_NEED), content_page=BLOG
    and count=INT.
    """

    class Meta:
        model = BlogItemContent

    content_type = factory.LazyAttribute(lambda obj: ContentType.objects.get_for_model(obj.item))
    object_id = factory.SelfAttribute("item.id")
    order = factory.Sequence(lambda n: n)


@restrict_factory(
    {
        "add_several_imagesblock": (Image,),
        "add_several_playsblock": (Play,),
        "add_several_personsblock": (Person,),
    }
)
class BlogFactory(factory.django.DjangoModelFactory):
    """
    Creates Blog Page.

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
    is_draft = factory.Faker("boolean", chance_of_getting_true=25)
    pub_date = factory.Faker("date_time", tzinfo=timezone.utc)
    title = factory.Faker("text", locale="ru_RU", max_nb_chars=50)

    @factory.post_generation
    def add_several_co_author(self, created, count, **kwargs):
        """Add specified count of co-authors to Blog."""
        if not created:
            return
        if count:
            BlogPersonFactory.create_batch(count, blog=self)

    @factory.post_generation
    def add_several_preamble(self, created, count, **kwargs):
        """Add specified count of Preamble item to Blog."""
        subfactory = factory.SubFactory(PreambleFactory)
        add_content_item_to_blog(self, created, count, subfactory)

    @factory.post_generation
    def add_several_text(self, created, count, **kwargs):
        """Add specified count of Text item to Blog."""
        subfactory = factory.SubFactory(TextFactory)
        add_content_item_to_blog(self, created, count, subfactory)

    @factory.post_generation
    def add_several_title(self, created, count, **kwargs):
        """Add specified count of Title item to Blog."""
        subfactory = factory.SubFactory(TitleFactory)
        add_content_item_to_blog(self, created, count, subfactory)

    @factory.post_generation
    def add_several_quote(self, created, count, **kwargs):
        """Add specified count of Quote item to Blog."""
        subfactory = factory.SubFactory(QuoteFactory)
        add_content_item_to_blog(self, created, count, subfactory)

    @factory.post_generation
    def add_several_personsblock(self, created, count, **kwargs):
        """Add specified count of content block with Persons to Blog."""
        subfactory = factory.SubFactory(PersonsBlockFactory)
        add_content_item_to_blog(self, created, count, subfactory)

    @factory.post_generation
    def add_several_imagesblock(self, created, count, **kwargs):
        """Add specified count of content block with Images to Blog."""
        subfactory = factory.SubFactory(ImagesBlockFactory)
        add_content_item_to_blog(self, created, count, subfactory)

    @factory.post_generation
    def add_several_playsblock(self, created, count, **kwargs):
        """Add specified count of content block with Plays to Blog."""
        subfactory = factory.SubFactory(PlaysBlockFactory)
        add_content_item_to_blog(self, created, count, subfactory)

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
