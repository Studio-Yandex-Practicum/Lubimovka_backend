from random import choice

import factory
from faker import Faker

from apps.core.decorators import restrict_factory
from apps.core.tests.factories import PersonFactory
from apps.info.models import Festival
from apps.library.models import (
    Achievement,
    Author,
    OtherLink,
    OtherPlay,
    Play,
    ProgramType,
    SocialNetworkLink,
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
        lambda: choice(SocialNetworkLink.SocialNetwork.choices)[0]
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

    name = factory.LazyFunction(lambda: fake["ru_RU"].word().capitalize())
    slug = factory.Faker("word", locale="en_US")


@restrict_factory({"global": [Festival, ProgramType]})
class PlayFactory(factory.django.DjangoModelFactory):
    """
    Create Play object.
    You should create at least one Festival and Program
    before use this factory.
    """

    class Meta:
        model = Play

    name = factory.LazyFunction(lambda: fake["ru_RU"].word().capitalize())
    city = factory.Faker("city_name", locale="ru_RU")
    year = factory.Faker("random_int", min=1990, max=2021, step=1)
    url_download = factory.Faker("url")
    url_reading = factory.Faker("url")
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
        Create a Play object and add it to other_plays_links field for Author.
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
