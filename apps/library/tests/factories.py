import random

import factory
import pytz
from faker import Faker

from apps.articles.models import Project
from apps.core.decorators import restrict_factory
from apps.core.models import Person, Role
from apps.core.tests.factories import ImageFactory, PersonFactory
from apps.info.models import Festival
from apps.library.models import (
    Achievement,
    Author,
    MasterClass,
    OtherLink,
    OtherPlay,
    ParticipationApplicationFestival,
    Performance,
    PerformanceMediaReview,
    PerformanceReview,
    Play,
    ProgramType,
    Reading,
    SocialNetworkLink,
    TeamMember,
)

fake = Faker("ru_RU")


class AchievementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Achievement

    tag = factory.Faker("word", locale="ru_RU")


@restrict_factory({"global": [Author]})
class SocialNetworkLinkFactory(factory.django.DjangoModelFactory):
    """
    Create SocialNetworkLink object.
    You should create at least one Author before use this factory.
    """

    class Meta:
        model = SocialNetworkLink

    author = factory.Iterator(Author.objects.all())
    name = factory.LazyFunction(
        lambda: random.choice(SocialNetworkLink.SocialNetwork.choices)[0]
    )
    link = factory.Faker("url")


@restrict_factory({"global": [Author]})
class OtherLinkFactory(factory.django.DjangoModelFactory):
    """
    Create OtherLink object.
    You should create at least one Author before use this factory.
    """

    class Meta:
        model = OtherLink

    author = factory.Iterator(Author.objects.all())
    name = factory.LazyFunction(lambda: fake["ru_RU"].word().capitalize())
    link = factory.Faker("url")
    is_pinned = factory.Faker("pybool")
    order_number = factory.Sequence(lambda x: x)


@restrict_factory({"global": [Author]})
class OtherPlayFactory(factory.django.DjangoModelFactory):
    """
    Create OtherPlay object.
    You should create at least one Author before use this factory.
    """

    class Meta:
        model = OtherPlay

    author = factory.Iterator(Author.objects.all())
    name = factory.LazyFunction(lambda: fake["ru_RU"].word().capitalize())
    link = factory.Faker("url")


class ProgramFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProgramType
        django_get_or_create = ["name"]

    name = factory.LazyFunction(lambda: fake.word().capitalize())


@restrict_factory({"global": [Festival, ProgramType]})
class PlayFactory(factory.django.DjangoModelFactory):
    """
    Create Play object.
    You should create at least one Festival and Program
    before use this factory.
    """

    class Meta:
        model = Play
        django_get_or_create = ["name"]

    name = factory.LazyFunction(lambda: fake["ru_RU"].word().capitalize())
    city = factory.Faker("city_name", locale="ru_RU")
    year = factory.Faker("random_int", min=1990, max=2021, step=1)
    url_download = factory.LazyAttribute(
        lambda obj: "www.plays-download/{}".format(obj.name)
    )
    url_reading = factory.LazyAttribute(
        lambda obj: "www.plays-reading/{}".format(obj.name)
    )
    program = factory.Iterator(ProgramType.objects.all())
    festival = factory.Iterator(Festival.objects.all())


@restrict_factory({"add_play": [Festival, ProgramType]})
class AuthorFactory(factory.django.DjangoModelFactory):
    """
    Creates Author objects.
    By default creates next fields:
        - person with full name, email, city and image;
        - quote;
        - biography.
    For other fields, use arguments:
        - add_achievement;
        - add_social_network_link;
        - add_other_link;
        - add_other_play;
        - add_play.
    For creation object with fully populated fields use complex_create method.
    """

    class Meta:
        model = Author

    person = factory.SubFactory(
        PersonFactory, add_email=True, add_city=True, add_image=True
    )
    quote = factory.Faker("sentence", nb_words=8, locale="ru_RU")
    biography = factory.Faker("text", locale="ru_RU")

    @factory.post_generation
    def add_achievement(self, created, extracted, **kwargs):
        """
        Create a Achievement object and add it
        to achievements field for Author.
        To use "add_achievement=True"
        """
        if not created:
            return
        if extracted:
            achievement = AchievementFactory.create()
            self.achievements.add(achievement)

    @factory.post_generation
    def add_social_network_link(self, created, extracted, **kwargs):
        """
        Create a SocialNetworkLink object and add it
        to social_networks field for Author.
        To use "add_social_network_link=True"
        """
        if not created:
            return
        if extracted:
            SocialNetworkLinkFactory.create(author=self)

    @factory.post_generation
    def add_other_link(self, created, extracted, **kwargs):
        """
        Create an OtherLink object and add it
        to other_links field for Author.
        To use "add_other_link=True"
        """
        if not created:
            return
        if extracted:
            OtherLinkFactory.create(author=self)

    @factory.post_generation
    def add_other_play(self, created, extracted, **kwargs):
        """
        Create an OtherPlayLink object and add it
        to other_plays_links field for Author.
        To use "add_other_play=True"
        """
        if not created:
            return
        if extracted:
            OtherPlayFactory.create(author=self)

    @factory.post_generation
    def add_play(self, created, extracted, **kwargs):
        """
        Create a Play object and add it to plays field for Author.
        You should create at least one Festival and Program
        before use this method.
        To use "add_play=True"
        """
        if not created:
            return
        if extracted:
            play = PlayFactory.create()
            self.plays.add(play)

    @classmethod
    def complex_create(cls):
        """
        Create Author object with fully populated fields.
        You should create at least one Festival and Program
        before use this method.
        """
        return cls.create(
            add_achievement=True,
            add_social_network_link=True,
            add_other_link=True,
            add_other_play=True,
            add_play=True,
        )


@restrict_factory({"global": [Person, Role]})
class TeamMemberFactory(factory.django.DjangoModelFactory):
    """
    Create TeamMember object.
    You should create at least one Person and Role
    before use this factory.
    This factory is started when you start the Reading,
    Performance or Master Class factory
    """

    class Meta:
        model = TeamMember

    person = factory.Iterator(Person.objects.all())
    role = factory.Iterator(Role.objects.all())


@restrict_factory({"global": [Person, Role]})
class MasterClassFactory(factory.django.DjangoModelFactory):
    """
    Create MasterClass object.
    You should create at least one Person and Role
    before use this factory.
    """

    class Meta:
        model = MasterClass

    name = factory.LazyFunction(lambda: fake.word().capitalize())
    description = factory.Faker("text", locale="ru_RU")
    member = factory.RelatedFactory(
        TeamMemberFactory,
        factory_related_name="masterclass",
        role__name="Ведущий",
    )
    project = factory.Iterator(Project.objects.all())


@restrict_factory({"global": [Person, Play, Project, Role]})
class PerformanceFactory(factory.django.DjangoModelFactory):
    """
    Create Performance object.
    You should create at least one Play and Project
    before use this factory.
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
        role__name="Драматург",
    )
    director = factory.RelatedFactory(
        TeamMemberFactory,
        factory_related_name="performance",
        role__name="Режиссёр",
    )
    project = factory.Iterator(Project.objects.all())

    @factory.post_generation
    def add_video(self, created, extracted, **kwargs):
        """
        Add video field for Performance
        To use "add_video=True"
        """
        if not created:
            return
        if extracted:
            self.video = factory.Faker("url", locale="ru_RU")

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
    def add_performance_review(self, created, extracted, **kwargs):
        """
        Create PerformanceReview object and add
        to reviews field for Performance.
        To use "add_performance_review=True"
        """
        if not created:
            return
        if extracted:
            PerformanceReviewFactory.create(performance=self)

    @factory.post_generation
    def add_performance_media_review(self, created, extracted, **kwargs):
        """
        Create PerformanceMediaReview object and add
        to media_reviews field for Performance.
        To use "add_performance_media_review=True"
        """
        if not created:
            return
        if extracted:
            PerformanceMediaReviewFactory.create(performance=self)

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
            add_performance_review=True,
            add_performance_media_review=True,
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
    # performance = factory.Iterator(Performance.objects.all())
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
    # performance = factory.Iterator(Performance.objects.all())
    url = factory.Faker("url")
    pub_date = factory.LazyFunction(
        lambda: fake.past_datetime(tzinfo=pytz.UTC)
    )


@restrict_factory({"global": [Person, Play, Project, Role]})
class ReadingFactory(factory.django.DjangoModelFactory):
    """
    Create Reading object.
    You should create at least one Play and Project
    before use this factory.
    """

    class Meta:
        model = Reading

    play = factory.Iterator(Play.objects.all())
    name = factory.LazyFunction(lambda: fake.word().capitalize())
    description = factory.Faker("text", locale="ru_RU")
    dramatist = factory.RelatedFactory(
        TeamMemberFactory,
        factory_related_name="reading",
        role__name="Драматург",
    )
    director = factory.RelatedFactory(
        TeamMemberFactory,
        factory_related_name="reading",
        role__name="Режиссёр",
    )
    project = factory.Iterator(Project.objects.all())


class ParticipationApplicationFestivalFactory(
    factory.django.DjangoModelFactory
):
    """
    Create ParticipationApplicationFestival object.
    """

    class Meta:
        model = ParticipationApplicationFestival

    first_name = factory.LazyFunction(lambda: fake.first_name())
    last_name = factory.LazyFunction(lambda: fake.last_name())
    birthday = factory.LazyFunction(
        lambda: fake.past_datetime(tzinfo=pytz.UTC)
    )
    city = factory.LazyFunction(lambda: fake.city_name())
    phone_number = factory.LazyFunction(lambda: fake.phone_number())
    email = factory.LazyFunction(lambda: fake.email())
    title = factory.LazyFunction(lambda: fake.word().capitalize())
    year = factory.LazyFunction(lambda: fake.year())
    file = factory.LazyAttribute(lambda obj: f"{obj.title}.txt")
