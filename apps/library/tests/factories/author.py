import factory
from faker import Faker

from apps.core.decorators import restrict_factory
from apps.core.tests.factories import PersonFactory
from apps.library.models import Achievement, Author, OtherLink, OtherPlay, Play, SocialNetworkLink

fake = Faker("ru_RU")


class AchievementFactory(factory.django.DjangoModelFactory):
    """Create Achievement object."""

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
    name = factory.Iterator((SocialNetworkLink.SocialNetwork.choices)[0])
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


@restrict_factory({"global": [Play]})
class AuthorFactory(factory.django.DjangoModelFactory):
    """
    Create Author object.

    By default creates next fields:
        - person with full name, email, city and image;
        - quote;
        - biography;
        - plays.
    For other fields, use arguments:
        - add_achievement;
        - add_social_network_link;
        - add_other_link;
        - add_other_play;
    For creation object with fully populated fields use complex_create method.
    """

    class Meta:
        model = Author

    person = factory.SubFactory(PersonFactory, add_email=True, add_city=True, add_image=True)
    quote = factory.Faker("sentence", nb_words=8, locale="ru_RU")
    biography = factory.Faker("text", locale="ru_RU")

    @factory.post_generation
    def add_achievement(self, created, extracted, **kwargs):
        """
        Create an Achievement object.

        Add it to achievements field for Author.
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
        Create a SocialNetworkLink object.

        Add it to social_networks field for Author.
        To use "add_social_network_link=True"
        """
        if not created:
            return
        if extracted:
            SocialNetworkLinkFactory.create(author=self)

    @factory.post_generation
    def add_other_link(self, created, extracted, **kwargs):
        """
        Create an OtherLink object.

        Add it to other_links field for Author.
        To use "add_other_link=True"
        """
        if not created:
            return
        if extracted:
            OtherLinkFactory.create(author=self)

    @factory.post_generation
    def add_other_play(self, created, extracted, **kwargs):
        """
        Create an OtherPlayLink object.

        Add it to other_plays_links field for Author.
        To use "add_other_play=True"
        """
        if not created:
            return
        if extracted:
            OtherPlayFactory.create(author=self)

    @factory.post_generation
    def plays(self, created, extracted, **kwargs):
        """
        Add a Play objects to plays field for Author.

        To add concrete plays use
        AuthorFactory.create(plays=(play1, play2, ...)).
        To add given number of Play objects use
        AuthorFactory.create(plays__num=<int>)
        """
        if not created:
            return
        if extracted:
            plays = extracted
            self.plays.add(*plays)
            return

        at_least = 1
        num = kwargs.get("num", None)
        how_many = num or at_least

        plays_count = Play.objects.count()
        how_many = min(plays_count, how_many)

        plays = Play.objects.order_by("?")[:how_many]
        self.plays.add(*plays)

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
        )
