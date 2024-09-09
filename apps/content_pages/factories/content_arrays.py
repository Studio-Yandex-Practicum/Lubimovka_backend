import factory

from apps.content_pages.factories import (
    ExtendedPersonFactory,
    NonpublishedOrderedPlayFactory,
    OrderedEventFactory,
    OrderedImageFactory,
    OrderedVideoFactory,
    PublishedOrderedPlayFactory,
)
from apps.content_pages.models import EventsBlock, ImagesBlock, PersonsBlock, PlaysBlock, VideosBlock


class ImagesBlockFactory(factory.django.DjangoModelFactory):
    """Create content block Image for blog, news or projects.

    Block creates with 3 ordered images.
    """

    class Meta:
        model = ImagesBlock

    title = factory.Faker("text", locale="ru_RU", max_nb_chars=20)

    @factory.post_generation
    def add_image(self, created, extracted, **kwargs):
        if created:
            OrderedImageFactory.create_batch(3, block=self)


class EventsBlockFactory(factory.django.DjangoModelFactory):
    """Create content block Event for projects.

    Block creates with 3 ordered events.
    """

    class Meta:
        model = EventsBlock

    title = factory.Faker("text", locale="ru_RU", max_nb_chars=20)

    @factory.post_generation
    def add_event(self, created, extracted, **kwargs):
        if created:
            OrderedEventFactory.create_batch(3, block=self)


class PersonsBlockFactory(factory.django.DjangoModelFactory):
    """Create content block Person for blog, news or projects.

    Block creates with 3 ordered persons.
    """

    class Meta:
        model = PersonsBlock

    title = factory.Faker("text", locale="ru_RU", max_nb_chars=20)

    @factory.post_generation
    def add_person(self, created, extracted, **kwargs):
        if created:
            ExtendedPersonFactory.create_batch(3, block=self)


class PlaysBlockFactory(factory.django.DjangoModelFactory):
    """Create content block Play for blog, news or projects.

    Block creates with 5 ordered plays.
    """

    class Meta:
        model = PlaysBlock

    title = factory.Faker("text", locale="ru_RU", max_nb_chars=20)

    @factory.post_generation
    def add_play(self, created, extracted, **kwargs):
        if created:
            PublishedOrderedPlayFactory.create_batch(3, block=self)
            NonpublishedOrderedPlayFactory.create_batch(2, block=self)


class VideosBlockFactory(factory.django.DjangoModelFactory):
    """Creates content block Video for projects.

    Block creates with 3 ordered videos.
    """

    class Meta:
        model = VideosBlock

    title = factory.Faker("text", locale="ru_RU", max_nb_chars=20)

    @factory.post_generation
    def add_video(self, created, extracted, **kwargs):
        if created:
            OrderedVideoFactory.create_batch(3, block=self)
