import random
from typing import Iterable
from zoneinfo import ZoneInfo

import factory
from django.conf import settings
from faker import Faker

from apps.afisha.models import Performance, PerformanceImage, PerformanceMediaReview, PerformanceReview
from apps.core.constants import AgeLimit, Status
from apps.core.decorators import restrict_factory
from apps.core.models import Person, Role
from apps.core.utils import get_picsum_image
from apps.info.utils import get_random_objects
from apps.library.factories import TeamMemberFactory
from apps.library.factories.constants import YOUTUBE_VIDEO_LINKS
from apps.library.models import Play

fake = Faker("ru_RU")


@restrict_factory(general=(Person, Play, Role))
class PerformanceFactory(factory.django.DjangoModelFactory):
    """Create Performance object.

    !!! The `events` field (the name also confuses: actually it's
    OneToOneField) is created by a signal in afisha app.

    Parameters:
    1. `without_video`: if True sets video to `None`.
    2. `add_real_images`: if True, tries to create object with real
    `main_image` and `bottom_image` images.
    3. `add_images_in_block`: if True create random number of images (no more
    than 8) and add them to `images_in_block` attribute
    4. `add_review`: if True create a set `PerformanceReview`
    5. `add_media_review`: if True create a set `PerformanceMediaReview`
    6. `add_team_members_with_roles`: waits for an iterable of strings. The
    strings should be a slug of any role. Selects random `Person` and add it to
    the `Performance` as team_member with the corresponding role.

    Class methods:
    1. `complex_create`:  shortcut. Run `create` method with parameters:
        add_video=True
        add_images_in_block=True
        add_review=True
        add_media_review=True

    Not obvious details:
    1. `dramatist_person` and `director_person`: it's not a model fields. It's a
    `hook`s to create `TeamMember` with roles "Драматург" and "Режиссер".
    """

    class Meta:
        model = Performance
        django_get_or_create = ("video",)

    class Params:
        without_video = factory.Trait(
            video=None,
        )
        add_real_images = factory.Trait(
            main_image=factory.django.ImageField(from_func=get_picsum_image),
            bottom_image=factory.django.ImageField(from_func=get_picsum_image),
        )

    name = factory.Faker("text", max_nb_chars=150, locale="ru_RU")
    main_image = factory.django.ImageField(
        color=factory.Faker("color"),
        width=factory.Faker("random_int", min=10, max=1000),
        height=factory.SelfAttribute("width"),
    )
    bottom_image = factory.django.ImageField(
        color=factory.Faker("color"),
        width=factory.Faker("random_int", min=10, max=1000),
        height=factory.SelfAttribute("width"),
    )
    description = factory.Faker("text", locale="ru_RU")
    text = factory.Faker("text", locale="ru_RU")
    age_limit = factory.LazyFunction(lambda: random.choice(list(AgeLimit)))
    video = factory.Iterator(YOUTUBE_VIDEO_LINKS)
    status = factory.LazyFunction(lambda: random.choice(list(Status)))

    @factory.lazy_attribute
    def play(self):
        return get_random_objects(Play.objects.filter(other_play=False))

    dramatist_person = factory.RelatedFactory(
        TeamMemberFactory,
        factory_related_name="performance",
        set_role_with_slug="dramatist",
    )
    director_person = factory.RelatedFactory(
        TeamMemberFactory,
        factory_related_name="performance",
        set_role_with_slug="director",
    )

    @factory.post_generation
    def add_images_in_block(self, created: bool, extracted: bool, **kwargs):
        """Create random amount of Image objects.

        And add them to images_in_block field for Performance.
        To use "add_images_in_block=True"
        """
        if created and extracted:
            images_count = random.randint(1, 9)
            PerformanceImageFactory.create_batch(images_count, performance=self)

    @factory.post_generation
    def add_review(self, created: bool, extracted: bool, **kwargs):
        """Create PerformanceReview object.

        And add to reviews field for Performance.
        To use "add_review=True"
        """
        if created and extracted:
            PerformanceReviewFactory.create(performance=self)

    @factory.post_generation
    def add_media_review(self, created: bool, extracted: bool, **kwargs):
        """Create PerformanceMediaReview object.

        And add to media_reviews field for Performance.
        To use "add_media_review=True"
        """
        if created and extracted:
            PerformanceMediaReviewFactory.create(performance=self)

    @factory.post_generation
    def add_team_members_with_roles(self, created, role_slugs: Iterable[str], **kwargs):
        """Add other team_members for created Reading object."""
        if not created:
            return
        if role_slugs:
            [TeamMemberFactory.create(reading=self, role_slug=role_slug) for role_slug in role_slugs]

    @classmethod
    def complex_create(cls, count=1, **kwargs):
        """Create Performance object with fully populated fields.

        You should create at least one Play and Project
        before use this method.
        """
        return cls.create_batch(
            count,
            add_images_in_block=True,
            add_review=True,
            add_media_review=True,
            **kwargs,
        )


@restrict_factory(general=(Performance,))
class PerformanceImageFactory(factory.django.DjangoModelFactory):
    """Create Images for Performance."""

    class Meta:
        model = PerformanceImage
        django_get_or_create = ("image",)

    image = factory.django.ImageField(
        color=factory.Faker("color"),
        width=factory.Faker("random_int", min=10, max=1000),
        height=factory.SelfAttribute("width"),
    )

    @factory.lazy_attribute
    def performance(self):
        return get_random_objects(Performance.objects.all())


@restrict_factory(general=(Performance,))
class PerformanceMediaReviewFactory(factory.django.DjangoModelFactory):
    """Create PerformanceMediaReview object."""

    class Meta:
        model = PerformanceMediaReview
        django_get_or_create = ("url",)

    class Params:
        add_real_image = factory.Trait(
            image=factory.django.ImageField(from_func=get_picsum_image),
        )

    media_name = factory.LazyFunction(lambda: fake.sentence(nb_words=random.choice([1, 2, 3])).capitalize())
    text = factory.Faker("text", locale="ru_RU")
    image = factory.django.ImageField(
        color=factory.Faker("color"),
        width=factory.Faker("random_int", min=10, max=1000),
        height=factory.SelfAttribute("width"),
    )
    url = factory.Faker("url")
    pub_date = factory.Faker("past_datetime", tzinfo=ZoneInfo(settings.TIME_ZONE))

    @factory.lazy_attribute
    def performance(self):
        return get_random_objects(Performance.objects.all())


@restrict_factory(general=(Performance,))
class PerformanceReviewFactory(factory.django.DjangoModelFactory):
    """Create PerformanceReview object."""

    class Meta:
        model = PerformanceReview
        django_get_or_create = ("url",)

    reviewer_name = factory.Faker("name", locale="ru_RU")
    text = factory.Faker("text", locale="ru_RU")
    url = factory.Faker("url")
    pub_date = factory.Faker("past_datetime", tzinfo=ZoneInfo(settings.TIME_ZONE))

    @factory.lazy_attribute
    def performance(self):
        return get_random_objects(Performance.objects.all())
