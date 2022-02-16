import factory
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from apps.articles.models import Project, ProjectContent
from apps.content_pages.tests.factories import (
    ImagesBlockFactory,
    LinkFactory,
    PerformancesBlockFactory,
    PersonsBlockFactory,
    PlaysBlockFactory,
    TextFactory,
    VideosBlockFactory,
)
from apps.core.decorators import restrict_factory
from apps.core.models import Person
from apps.library.models.play import Play


def add_content_item_to_project(project, created, count, factory):
    """Add specified count of content item or block to Project."""
    if not created:
        return
    if count:
        ProjectContentFactory.create_batch(count, item=factory, content_page=project)


class ProjectContentFactory(factory.django.DjangoModelFactory):
    """Base model for content items and blocks for Project.

    When add content to Project (via add_content_item_to_project - see above)
    you should add item=factory.SubFactory(BLOCK_OR_ITEM_FACTORY_YOU_NEED),
    content_page=PROJECT and count=INT.
    """

    class Meta:
        model = ProjectContent

    content_type = factory.LazyAttribute(lambda obj: ContentType.objects.get_for_model(obj.item))
    object_id = factory.SelfAttribute("item.id")
    order = factory.Sequence(lambda n: n)


@restrict_factory(
    add_several_playsblock=(Play,),
    add_several_personsblock=(Person,),
)
class ProjectFactory(factory.django.DjangoModelFactory):
    """Creates Project Page.

    You can customize Project's content by adding method and count when
    create (e.g. 'ProjectFactory.create(add_several_preamble=5,
    add_several_personsblock=3)). Content item/block will not be
    created if relevant method are not mentioned.
    You can use 'complex_create' which will create all content item/block
    each in single copy.
    """

    class Meta:
        model = Project

    description = factory.Faker(
        "paragraph",
        locale="ru_RU",
        nb_sentences=5,
        variable_nb_sentences=False,
    )
    image = factory.django.ImageField(color=factory.Faker("color"))
    intro = factory.Faker("sentence", locale="ru_RU", nb_words=12)
    is_draft = factory.Faker("boolean", chance_of_getting_true=25)
    pub_date = factory.Faker("date_time", tzinfo=timezone.utc)
    title = factory.Faker("text", locale="ru_RU", max_nb_chars=50)

    @factory.post_generation
    def add_several_links(self, created, count, **kwargs):
        """Add specified count of Links item to Project."""
        subfactory = factory.SubFactory(LinkFactory)
        add_content_item_to_project(self, created, count, subfactory)

    @factory.post_generation
    def add_several_text(self, created, count, **kwargs):
        """Add specified count of Text item to Project."""
        subfactory = factory.SubFactory(TextFactory)
        add_content_item_to_project(self, created, count, subfactory)

    @factory.post_generation
    def add_several_personsblock(self, created, count, **kwargs):
        """Add specified count of content block with Persons to Project."""
        subfactory = factory.SubFactory(PersonsBlockFactory)
        add_content_item_to_project(self, created, count, subfactory)

    @factory.post_generation
    def add_several_imagesblock(self, created, count, **kwargs):
        """Add specified count of content block with Images to Project."""
        subfactory = factory.SubFactory(ImagesBlockFactory)
        add_content_item_to_project(self, created, count, subfactory)

    @factory.post_generation
    def add_several_playsblock(self, created, count, **kwargs):
        """Add specified count of content block with Plays to Project."""
        subfactory = factory.SubFactory(PlaysBlockFactory)
        add_content_item_to_project(self, created, count, subfactory)

    @factory.post_generation
    def add_several_videosblock(self, created, count, **kwargs):
        """Add specified count of content block with Video to Project."""
        subfactory = factory.SubFactory(VideosBlockFactory)
        add_content_item_to_project(self, created, count, subfactory)

    @factory.post_generation
    def add_several_performancesblock(self, created, count, **kwargs):
        """Add specified count of content block with Performances to Project."""
        subfactory = factory.SubFactory(PerformancesBlockFactory)
        add_content_item_to_project(self, created, count, subfactory)

    @classmethod
    def complex_create(cls, count):
        """Create specified count of Project with fully populated content."""
        return cls.create_batch(
            count,
            add_several_text=1,
            add_several_links=1,
            add_several_playsblock=1,
            add_several_imagesblock=1,
            add_several_personsblock=1,
            add_several_videosblock=1,
            add_several_performancesblock=1,
        )
