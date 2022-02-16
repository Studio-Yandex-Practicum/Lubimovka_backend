import factory

from apps.core.decorators import restrict_factory
from apps.core.models import Person, Role
from apps.library.models import Performance, Play

from ..factories.content_items import ImageForContentFactory, VideoFactory
from ..models import (
    ContentPersonRole,
    ExtendedPerson,
    ImagesBlock,
    OrderedImage,
    OrderedPerformance,
    OrderedPlay,
    OrderedVideo,
    PerformancesBlock,
    PlaysBlock,
    VideosBlock,
)


@restrict_factory({"global": (Role,)})
class ContentPersonRoleFactory(factory.django.DjangoModelFactory):
    """
    Creates 'through' object with attrs ExtendedPerson and Role.

    For using in ExtendedPersonFactory.
    """

    class Meta:
        model = ContentPersonRole

    role = factory.Iterator(Role.objects.all())


@restrict_factory({"global": (Person,)})
class ExtendedPersonFactory(factory.django.DjangoModelFactory):
    """
    Create Person with order and role for block.

    You should create at least one Person and Role before
    using factory. Order in factory assume that there are not
    more than 3 ordered persons in a block.
    """

    class Meta:
        model = ExtendedPerson

    order = factory.Sequence(lambda n: (n % 3 + 1))
    person = factory.Iterator(Person.objects.all())

    @factory.post_generation
    def add_roles(self, created, extracted, **kwargs):
        """Add two roles to Person."""
        if not created:
            return
        ContentPersonRoleFactory.create_batch(2, extended_person=self)


class OrderedImageFactory(factory.django.DjangoModelFactory):
    """Create Image with order for block.

    Order in factory assumes that there are not more than 3 ordered images in a block.
    """

    class Meta:
        model = OrderedImage

    block = factory.Iterator(ImagesBlock.objects.all())
    item = factory.SubFactory(ImageForContentFactory)
    order = factory.Sequence(lambda n: (n % 3 + 1))


@restrict_factory({"global": (Performance,)})
class OrderedPerformanceFactory(factory.django.DjangoModelFactory):
    """
    Creates Performance with order for block.

    Order in factory assume that there are not more than 3 ordered performances in a block.
    """

    class Meta:
        model = OrderedPerformance

    block = factory.Iterator(PerformancesBlock.objects.all())
    item = factory.Iterator(Performance.objects.all())
    order = factory.Sequence(lambda n: (n % 3 + 1))


@restrict_factory({"global": (Play,)})
class OrderedPlayFactory(factory.django.DjangoModelFactory):
    """
    Creates Play with order for block.

    Order in factory assume that there are not more than 3 ordered plays in a block.
    """

    class Meta:
        model = OrderedPlay

    block = factory.Iterator(PlaysBlock.objects.all())
    item = factory.Iterator(Play.objects.all())
    order = factory.Sequence(lambda n: (n % 3 + 1))


class OrderedVideoFactory(factory.django.DjangoModelFactory):
    """
    Creates Video with order for block.

    Order in factory assume that there are not more than 3 ordered videos in a block.
    """

    class Meta:
        model = OrderedVideo

    block = factory.Iterator(VideosBlock.objects.all())
    item = factory.SubFactory(VideoFactory)
    order = factory.Sequence(lambda n: (n % 3 + 1))
