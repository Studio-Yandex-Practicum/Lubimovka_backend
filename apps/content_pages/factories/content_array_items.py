import random

import factory

from apps.afisha.models import Event
from apps.content_pages.models import (
    ContentPersonRole,
    ExtendedPerson,
    OrderedEvent,
    OrderedImage,
    OrderedPlay,
    OrderedVideo,
    PersonsBlock,
)
from apps.core.decorators import restrict_factory
from apps.core.models import Person, Role
from apps.core.utils import get_picsum_image
from apps.info.utils import get_random_objects_by_model, get_random_objects_by_queryset
from apps.library.factories.constants import YOUTUBE_VIDEO_LINKS
from apps.library.models import Play


@restrict_factory(general=(Role,))
class ContentPersonRoleFactory(factory.django.DjangoModelFactory):
    """Create 'through' object with attrs ExtendedPerson and Role.

    For using in ExtendedPersonFactory.
    """

    class Meta:
        model = ContentPersonRole
        django_get_or_create = ("extended_person", "role")

    @factory.lazy_attribute
    def role(self):
        return get_random_objects_by_model(Role)

    @factory.lazy_attribute
    def extended_person(self):
        return get_random_objects_by_model(ExtendedPerson)


@restrict_factory(general=(Person,))
class ExtendedPersonFactory(factory.django.DjangoModelFactory):
    """Create Person with order and role for `ContentArrayPerson` o.

    Order in factory assume that there are not
    more than 3 ordered persons in a block.
    """

    class Meta:
        model = ExtendedPerson
        django_get_or_create = ("block", "person")

    order = factory.Sequence(lambda n: (n % 3 + 1))

    @factory.lazy_attribute
    def person(self):
        return get_random_objects_by_model(Person)

    @factory.lazy_attribute
    def block(self):
        return get_random_objects_by_model(PersonsBlock)

    @factory.post_generation
    def add_roles(self, created, extracted, **kwargs):
        """Add two roles to Person."""
        if created:
            ContentPersonRoleFactory.create_batch(2, extended_person=self)


class OrderedImageFactory(factory.django.DjangoModelFactory):
    """Create Image with order for block.

    Order in factory assume that there are not more than 3 ordered images in a block.

    Parameters:
    1. `add_real_image` — if True, tries to create object with real image
    2. `empty_title` - if True, create OrderedImage objects with empty title
    """

    class Meta:
        model = OrderedImage

    class Params:
        empty_title = factory.Trait(title="")
        add_real_image = factory.Trait(
            image=factory.django.ImageField(from_func=get_picsum_image),
        )

    title = factory.Faker("sentence", locale="ru_RU")
    image = factory.django.ImageField(color=factory.Faker("color"))
    order = factory.Sequence(lambda n: (n % 3 + 1))


@restrict_factory(general=(Event,))
class OrderedEventFactory(factory.django.DjangoModelFactory):
    """Create Events with order for block.

    Order in factory assume that there are not more than 3 ordered events in a block.
    """

    class Meta:
        model = OrderedEvent

    order = factory.Sequence(lambda n: (n % 3 + 1))

    @factory.lazy_attribute
    def item(self):
        return get_random_objects_by_queryset(Event.objects.filter(type=Event.EventType.PERFORMANCE))


@restrict_factory(general=(Play,))
class OrderedPlayFactory(factory.django.DjangoModelFactory):
    """Create Play with order for block.

    Order in factory assume that there are not more than 3 ordered plays in a block.
    """

    class Meta:
        model = OrderedPlay

    order = factory.Sequence(lambda n: (n % 3 + 1))

    @factory.lazy_attribute
    def item(self):
        return get_random_objects_by_queryset(Play.objects.filter(other_play=False))


class OrderedVideoFactory(factory.django.DjangoModelFactory):
    """Create Video with order for block.

    Order in factory assume that there are not more than 3 ordered videos in a block.
    Parameters:
    1. `empty_title` - if True, create OrderedVideo objects with empty title
    """

    class Meta:
        model = OrderedVideo

    class Params:
        empty_title = factory.Trait(title="")

    title = factory.Faker("sentence", locale="ru_RU")
    url = factory.LazyFunction(lambda: random.choice(YOUTUBE_VIDEO_LINKS))
    order = factory.Sequence(lambda n: (n % 3 + 1))
