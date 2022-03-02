from zoneinfo import ZoneInfo

import factory
from django.conf import settings

from apps.articles.models import NewsItem, NewsItemContent
from apps.content_pages.factories import AbstractContentFactory
from apps.core.decorators import restrict_factory
from apps.core.models import Person
from apps.library.models.play import Play


@restrict_factory(general=(NewsItem,))
class NewsItemContentModuleFactory(AbstractContentFactory):
    """ContentModule factory for `NewsItem`.

    1. Set relation to `NewsItem` object.
    2. The factory inherits generic relations to `ContentUnit` and `ContentArray`
    objects form `AbstractContentFactory`.
    """

    class Meta:
        model = NewsItemContent

    @factory.lazy_attribute
    def content_page(self):
        return NewsItemContent.objects.order_by("?").first()


@restrict_factory(
    add_several_playsblock=(Play,),
    add_several_personsblock=(Person,),
)
class NewsItemFactory(factory.django.DjangoModelFactory):
    """Creates News Page.

    You can customize News content by adding method and count when
    create (e.g. 'NewsItemFactory.create(add_several_preamble=5,
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
    pub_date = factory.Faker("date_time", tzinfo=ZoneInfo(settings.TIME_ZONE))
    title = factory.Faker("text", locale="ru_RU", max_nb_chars=50)

    @factory.post_generation
    def add_several_imagesblock(self, created, count, **kwargs):
        """Add specified count of content block with Images to News."""
        if created and count:
            NewsItemContentModuleFactory.create_batch(
                count,
                content_page=self,
                array_image=True,
            )

    @factory.post_generation
    def add_several_personsblock(self, created, count, **kwargs):
        """Add specified count of content block with Persons to News."""
        if created and count:
            NewsItemContentModuleFactory.create_batch(count, content_page=self, array_person=True)

    @factory.post_generation
    def add_several_playsblock(self, created, count, **kwargs):
        """Add specified count of content block with Plays to News."""
        if created and count:
            NewsItemContentModuleFactory.create_batch(count, content_page=self, array_play=True)

    @factory.post_generation
    def add_several_preamble(self, created, count, **kwargs):
        """Add specified count of Preamble item to News."""
        if created and count:
            NewsItemContentModuleFactory.create_batch(count, content_page=self, unit_preamble=True)

    @factory.post_generation
    def add_several_quote(self, created, count, **kwargs):
        """Add specified count of Quote item to News."""
        if created and count:
            NewsItemContentModuleFactory.create_batch(count, content_page=self, unit_quote=True)

    @factory.post_generation
    def add_several_text(self, created, count, **kwargs):
        """Add specified count of Text item to News."""
        if created and count:
            NewsItemContentModuleFactory.create_batch(count, content_page=self, unit_text=True)

    @factory.post_generation
    def add_several_title(self, created, count, **kwargs):
        """Add specified count of Title item to News."""
        if created and count:
            NewsItemContentModuleFactory.create_batch(count, content_page=self, unit_title=True)

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
