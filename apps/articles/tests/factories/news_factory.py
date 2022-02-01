import factory
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from apps.articles.models import NewsItem, NewsItemContent
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
from apps.core.models import Person
from apps.library.models.play import Play


def add_content_item_to_news(news, created, count, factory):
    """Add specified count of content item or block to News."""
    if not created:
        return
    if count:
        NewsItemContentFactory.create_batch(count, item=factory, content_page=news)


class NewsItemContentFactory(factory.django.DjangoModelFactory):
    """
    Base model for content items and blocks for News.

    When add content to News (via add_content_item_to_news - see above) you should add
    item=factory.SubFactory(BLOCK_OR_ITEM_FACTORY_YOU_NEED), content_page=NEWS
    and count=INT.
    """

    class Meta:
        model = NewsItemContent

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
class NewsFactory(factory.django.DjangoModelFactory):
    """
    Creates News Page.

    You can customize News content by adding method and count when
    create (e.g. 'NewsFactory.create(add_several_preamble=5,
    add_several_personsblock=3)). Content item/block will not be
    created if relevant method are not mentioned.
    You can use 'complex_create' which will create all content item/block
    each in single copy.
    """

    class Meta:
        model = NewsItem

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
    def add_several_preamble(self, created, count, **kwargs):
        """Add specified count of Preamble item to News."""
        subfactory = factory.SubFactory(PreambleFactory)
        add_content_item_to_news(self, created, count, subfactory)

    @factory.post_generation
    def add_several_text(self, created, count, **kwargs):
        """Add specified count of Text item to News."""
        subfactory = factory.SubFactory(TextFactory)
        add_content_item_to_news(self, created, count, subfactory)

    @factory.post_generation
    def add_several_title(self, created, count, **kwargs):
        """Add specified count of Title item to News."""
        subfactory = factory.SubFactory(TitleFactory)
        add_content_item_to_news(self, created, count, subfactory)

    @factory.post_generation
    def add_several_quote(self, created, count, **kwargs):
        """Add specified count of Quote item to News."""
        subfactory = factory.SubFactory(QuoteFactory)
        add_content_item_to_news(self, created, count, subfactory)

    @factory.post_generation
    def add_several_personsblock(self, created, count, **kwargs):
        """Add specified count of content block with Persons to News."""
        subfactory = factory.SubFactory(PersonsBlockFactory)
        add_content_item_to_news(self, created, count, subfactory)

    @factory.post_generation
    def add_several_imagesblock(self, created, count, **kwargs):
        """Add specified count of content block with Images to News."""
        subfactory = factory.SubFactory(ImagesBlockFactory)
        add_content_item_to_news(self, created, count, subfactory)

    @factory.post_generation
    def add_several_playsblock(self, created, count, **kwargs):
        """Add specified count of content block with Plays to News."""
        subfactory = factory.SubFactory(PlaysBlockFactory)
        add_content_item_to_news(self, created, count, subfactory)

    @classmethod
    def complex_create(cls, count):
        """Create specified count of News with fully populated content."""
        return cls.create_batch(
            count,
            add_several_preamble=1,
            add_several_text=1,
            add_several_title=1,
            add_several_quote=1,
            add_several_playsblock=1,
            add_several_imagesblock=1,
            add_several_personsblock=1,
        )
