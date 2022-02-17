import factory

from apps.content_pages.factories.content_array_items import (
    ExtendedPersonFactory,
    OrderedImageFactory,
    OrderedPerformanceFactory,
    OrderedPlayFactory,
    OrderedVideoFactory,
)
from apps.content_pages.models import ImagesBlock, PerformancesBlock, PersonsBlock, PlaysBlock, VideosBlock


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


class PerformancesBlockFactory(factory.django.DjangoModelFactory):
    """Create content block Performance for projects.

    Block creates with 3 ordered performances.
    """

    class Meta:
        model = PerformancesBlock

    title = factory.Faker("text", locale="ru_RU", max_nb_chars=20)

    @factory.post_generation
    def add_performance(self, created, extracted, **kwargs):
        if created:
            OrderedPerformanceFactory.create_batch(3, block=self)


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

    Block creates with 3 ordered plays.
    """

    class Meta:
        model = PlaysBlock

    title = factory.Faker("text", locale="ru_RU", max_nb_chars=20)

    @factory.post_generation
    def add_play(self, created, extracted, **kwargs):
        if created:
            OrderedPlayFactory.create_batch(3, block=self)


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
