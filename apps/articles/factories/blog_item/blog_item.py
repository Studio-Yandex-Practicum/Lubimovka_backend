import factory
from django.utils import timezone

from apps.articles.models import BlogItem, BlogPerson
from apps.content_pages.models import Image
from apps.core.decorators import restrict_factory
from apps.core.models import Person, Role
from apps.library.models.play import Play

from .blog_item_content import (
    BlogItemImagesBlockContentFactory,
    BlogItemPersonsBlockContentFactory,
    BlogItemPlaysBlockContentFactory,
    BlogItemPreambleContentFactory,
    BlogItemQuoteContentFactory,
    BlogItemTextContentFactory,
    BlogItemTitleContentFactory,
)


def add_content_item_to_blog(blog_item, created, count, factory_class):
    """Add specified count of content item or block to Blog."""
    if not created:
        return
    if count:
        factory_class.create_batch(count, content_page=blog_item)


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


@restrict_factory(
    {
        "add_several_imagesblock": (Image,),
        "add_several_playsblock": (Play,),
        "add_several_personsblock": (Person,),
    }
)
class BlogItemFactory(factory.django.DjangoModelFactory):
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
    def add_several_imagesblock(self, created, count, **kwargs):
        """Add specified count of content block with Images to Blog."""
        add_content_item_to_blog(
            blog_item=self,
            created=created,
            count=count,
            factory_class=BlogItemImagesBlockContentFactory,
        )

    @factory.post_generation
    def add_several_personsblock(self, created, count, **kwargs):
        """Add specified count of content block with Persons to Blog."""
        add_content_item_to_blog(
            blog_item=self,
            created=created,
            count=count,
            factory_class=BlogItemPersonsBlockContentFactory,
        )

    @factory.post_generation
    def add_several_playsblock(self, created, count, **kwargs):
        """Add specified count of content block with Plays to Blog."""
        add_content_item_to_blog(
            blog_item=self,
            created=created,
            count=count,
            factory_class=BlogItemPlaysBlockContentFactory,
        )

    @factory.post_generation
    def add_several_preamble(self, created, count, **kwargs):
        """Add specified count of Preamble item to Blog."""
        add_content_item_to_blog(
            blog_item=self,
            created=created,
            count=count,
            factory_class=BlogItemPreambleContentFactory,
        )

    @factory.post_generation
    def add_several_quote(self, created, count, **kwargs):
        """Add specified count of Quote item to Blog."""
        add_content_item_to_blog(
            blog_item=self,
            created=created,
            count=count,
            factory_class=BlogItemQuoteContentFactory,
        )

    @factory.post_generation
    def add_several_text(self, created, count, **kwargs):
        """Add specified count of Text item to Blog."""
        add_content_item_to_blog(
            blog_item=self,
            created=created,
            count=count,
            factory_class=BlogItemTextContentFactory,
        )

    @factory.post_generation
    def add_several_title(self, created, count, **kwargs):
        """Add specified count of Title item to Blog."""
        add_content_item_to_blog(
            blog_item=self,
            created=created,
            count=count,
            factory_class=BlogItemTitleContentFactory,
        )

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
