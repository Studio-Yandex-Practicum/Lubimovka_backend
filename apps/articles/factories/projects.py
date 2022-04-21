import random
from zoneinfo import ZoneInfo

import factory
from django.conf import settings

from apps.afisha.models import Event
from apps.articles.models import Project, ProjectContent
from apps.content_pages.factories import AbstractContentFactory
from apps.core.constants import Status
from apps.core.decorators import restrict_factory
from apps.core.models import Person
from apps.library.models.play import Play


@restrict_factory(general=(Project,))
class ProjectContentModuleFactory(AbstractContentFactory):
    """ContentModule factory for `Project`.

    1. Set relation to `Project` object.
    2. The factory inherits generic relations to `ContentUnit` and `ContentArray`
    objects form `AbstractContentFactory`.
    """

    class Meta:
        model = ProjectContent

    @factory.lazy_attribute
    def content_page(self):
        return Project.objects.order_by("?").first()


@restrict_factory(
    add_several_events=(Event,),
    add_several_playsblock=(Play,),
    add_several_personsblock=(Person,),
)
class ProjectFactory(factory.django.DjangoModelFactory):
    """Creates Project Page.

    You can customize Project's content by adding method and count when
    create (e.g. 'ProjectFactory.create(add_several_rich_text=5,
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
    pub_date = factory.Faker("date_time", tzinfo=ZoneInfo(settings.TIME_ZONE))
    title = factory.Faker("text", locale="ru_RU", max_nb_chars=50)
    status = factory.LazyFunction(lambda: random.choice(list(Status)))

    @factory.post_generation
    def add_several_imagesblock(self, created, count, **kwargs):
        """Add specified count of content block with Images to Project."""
        if created and count:
            ProjectContentModuleFactory.create_batch(count, content_page=self, array_image=True)

    @factory.post_generation
    def add_several_links(self, created, count, **kwargs):
        """Add specified count of Links item to Project."""
        if created and count:
            ProjectContentModuleFactory.create_batch(count, content_page=self, unit_link=True)

    @factory.post_generation
    def add_several_eventsblock(self, created, count, **kwargs):
        """Add specified count of content block with Events to Project."""
        if created and count:
            ProjectContentModuleFactory.create_batch(count, content_page=self, array_event=True)

    @factory.post_generation
    def add_several_personsblock(self, created, count, **kwargs):
        """Add specified count of content block with Persons to Project."""
        if created and count:
            ProjectContentModuleFactory.create_batch(count, content_page=self, array_person=True)

    @factory.post_generation
    def add_several_playsblock(self, created, count, **kwargs):
        """Add specified count of content block with Plays to Project."""
        if created and count:
            ProjectContentModuleFactory.create_batch(count, content_page=self, array_play=True)

    @factory.post_generation
    def add_several_rich_text(self, created, count, **kwargs):
        """Add specified count of RichText unit."""
        if created and count:
            ProjectContentModuleFactory.create_batch(count, content_page=self, unit_rich_text=True)

    @factory.post_generation
    def add_several_videosblock(self, created, count, **kwargs):
        """Add specified count of content block with Video to Project."""
        if created and count:
            ProjectContentModuleFactory.create_batch(count, content_page=self, array_video=True)

    @classmethod
    def complex_create(cls, count, **kwargs):
        """Create specified count of Project with fully populated content."""
        return cls.create_batch(
            count,
            add_several_eventsblock=1,
            add_several_imagesblock=1,
            add_several_links=1,
            add_several_playsblock=1,
            add_several_personsblock=1,
            add_several_rich_text=1,
            add_several_videosblock=1,
            **kwargs,
        )
