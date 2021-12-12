import random

import factory
import pytz
from faker import Faker

from apps.core.decorators import restrict_factory
from apps.core.models import Person, Role
from apps.core.tests.factories import ImageFactory
from apps.library.models import (
    Performance,
    PerformanceMediaReview,
    PerformanceReview,
    Play,
)

from .team_member import TeamMemberFactory

fake = Faker("ru_RU")


@restrict_factory({"global": [Person, Play, Role]})
class PerformanceFactory(factory.django.DjangoModelFactory):
    """
    Create Performance object.
    You should create at least one Play, one Person and one Role
    before use this factory.
    By default creates next fields:
        name; play; main_image; bottom_image; description; text; age_limit;
        two team_members: dramatist; director.
    For other fields, use arguments:
        - add_video;
        - add_images_in_block;
        - add_review;
        - add_media_review;
    For adding other team_members use:
        - add_team_members=(text_adaptation, actor, ...)
    For creation object with fully populated fields use complex_create method.
    """

    class Meta:
        model = Performance

    name = factory.LazyFunction(lambda: fake.word().capitalize())
    play = factory.Iterator(Play.objects.all())
    main_image = factory.django.ImageField(
        color=factory.LazyFunction(
            lambda: random.choice(["blue", "yellow", "green", "orange"])
        ),
        width=factory.LazyFunction(lambda: random.randint(10, 1000)),
        height=factory.SelfAttribute("width"),
    )
    bottom_image = factory.django.ImageField(
        color=factory.LazyFunction(
            lambda: random.choice(["blue", "yellow", "green", "orange"])
        ),
        width=factory.LazyFunction(lambda: random.randint(10, 1000)),
        height=factory.SelfAttribute("width"),
    )
    description = factory.Faker("text", locale="ru_RU")
    text = factory.Faker("text", locale="ru_RU")
    age_limit = factory.LazyFunction(lambda: random.randint(0, 18))
    dramatist = factory.RelatedFactory(
        TeamMemberFactory,
        factory_related_name="performance",
        role__slug="dramatist",
    )
    director = factory.RelatedFactory(
        TeamMemberFactory,
        factory_related_name="performance",
        role__slug="director",
    )

    @factory.post_generation
    def add_video(self, created, extracted, **kwargs):
        """
        Add video field for Performance
        To use "add_video=True"
        """
        if not created:
            return
        if extracted:
            self.video = fake.url()

    @factory.post_generation
    def add_images_in_block(self, created, extracted, **kwargs):
        """
        Create random amount of Image objects and add them
        to images_in_block field for Performance.
        To use "add_images_in_block=True"
        """
        if not created:
            return
        if extracted:
            for _ in range(random.randint(1, 8)):
                image = ImageFactory.create()
                self.images_in_block.add(image)

    @factory.post_generation
    def add_review(self, created, extracted, **kwargs):
        """
        Create PerformanceReview object and add
        to reviews field for Performance.
        To use "add_review=True"
        """
        if not created:
            return
        if extracted:
            PerformanceReviewFactory.create(performance=self)

    @factory.post_generation
    def add_media_review(self, created, extracted, **kwargs):
        """
        Create PerformanceMediaReview object and add
        to media_reviews field for Performance.
        To use "add_media_review=True"
        """
        if not created:
            return
        if extracted:
            PerformanceMediaReviewFactory.create(performance=self)

    @factory.post_generation
    def add_team_members(self, created, extracted, **kwargs):
        if not created:
            return
        if extracted:
            roles = extracted
            for role in roles:
                self.team_members.add(
                    TeamMemberFactory(
                        performance=self,
                        role__slug=f"{role}",
                    )
                )

    @classmethod
    def complex_create(cls):
        """
        Create Performance object with fully populated fields.
        You should create at least one Play and Project
        before use this method.
        """
        return cls.create(
            add_video=True,
            add_images_in_block=True,
            add_review=True,
            add_media_review=True,
        )


@restrict_factory({"global": [Performance]})
class PerformanceMediaReviewFactory(factory.django.DjangoModelFactory):
    """
    Create PerformanceMediaReview object.
    You should create at least one Performance
    before use this factory.
    """

    class Meta:
        model = PerformanceMediaReview

    media_name = factory.LazyFunction(
        lambda: fake.sentence(nb_words=random.choice([1, 2, 3])).capitalize()
    )
    text = factory.Faker("text", locale="ru_RU")
    image = factory.django.ImageField(
        color=factory.LazyFunction(
            lambda: random.choice(["blue", "yellow", "green", "orange"])
        ),
        width=factory.LazyFunction(lambda: random.randint(10, 1000)),
        height=factory.SelfAttribute("width"),
    )
    performance = factory.Iterator(Performance.objects.all())
    url = factory.Faker("url")
    pub_date = factory.LazyFunction(
        lambda: fake.past_datetime(tzinfo=pytz.UTC)
    )


@restrict_factory({"global": [Performance]})
class PerformanceReviewFactory(factory.django.DjangoModelFactory):
    """
    Create PerformanceReview object.
    You should create at least one Performance
    before use this factory.
    """

    class Meta:
        model = PerformanceReview

    reviewer_name = factory.Faker("name", locale="ru_RU")
    text = factory.Faker("text", locale="ru_RU")
    performance = factory.Iterator(Performance.objects.all())
    url = factory.Faker("url")
    pub_date = factory.LazyFunction(
        lambda: fake.past_datetime(tzinfo=pytz.UTC)
    )
