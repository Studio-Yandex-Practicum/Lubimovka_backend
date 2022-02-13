from typing import Iterable

import factory
from faker import Faker

from apps.core.decorators import restrict_factory
from apps.info.models import Festival, Person
from apps.library.models import Achievement, Author, OtherLink, OtherPlay, Play, ProgramType, SocialNetworkLink

fake = Faker("ru_RU")


class AchievementFactory(factory.django.DjangoModelFactory):
    """Create Achievement object."""

    class Meta:
        model = Achievement

    tag = factory.Faker("word", locale="ru_RU")


@restrict_factory({"global": (Author,)})
class SocialNetworkLinkFactory(factory.django.DjangoModelFactory):
    """Create SocialNetworkLink object."""

    class Meta:
        model = SocialNetworkLink
        django_get_or_create = ("author", "name")

    name = factory.Iterator(SocialNetworkLink.SocialNetwork.values)
    link = factory.Faker("url")

    @factory.lazy_attribute
    def author(self):
        return Author.objects.order_by("?").first()


@restrict_factory({"global": (Author,)})
class OtherLinkFactory(factory.django.DjangoModelFactory):
    """Create OtherLink object."""

    class Meta:
        model = OtherLink
        django_get_or_create = ("author", "name")

    name = factory.LazyFunction(lambda: fake["ru_RU"].word().capitalize())
    link = factory.Faker("url")
    is_pinned = factory.Faker("pybool")
    order_number = factory.Sequence(lambda index: index)

    @factory.lazy_attribute
    def author(self):
        return Author.objects.order_by("?").first()


@restrict_factory({"global": (Author,)})
class OtherPlayFactory(factory.django.DjangoModelFactory):
    """Create OtherPlay object."""

    class Meta:
        model = OtherPlay
        django_get_or_create = ("author", "name")

    name = factory.LazyFunction(lambda: fake["ru_RU"].word().capitalize())
    link = factory.Faker("url")

    @factory.lazy_attribute
    def author(self):
        return Author.objects.order_by("?").first()


@restrict_factory({"global": (Play, Person, Festival, ProgramType)})
class AuthorFactory(factory.django.DjangoModelFactory):
    """Create Author object.

    Parameters:
    1. `add_several_achievement`: create <int> `Achievement` objects, link to `Author`.
    2. `add_several_social_network_link`:  create <int> `SocialNetworkLink` objects, link to `Author`.
    3. `add_several_other_link`: create <int> `OtherLink` objects, link to `Author`.
    4. `add_several_other_play`: create <int> `OtherPlay` objects, link to `Author`.
    5. `plays`: wait for Iterable[Play]. Link the `Play` objects to `Author`.
    6. `plays__num`: select <num> `Play` objects and link them to `Author`.

    Class methods:
    1. `complex_create`:  shortcut. Create `Author` with fully populated fields.

    The fields `city`, `email`, `image` has to be filled in the `Person` object.
    Otherwise, it should not be associated with the `Author`.

    Author object is linked to `Achievement`, `SocialNetworkLink`, `OtherLink`,
    `OtherPlay` objects with m2m connection. These models aren't used elsewhere.
    It's ok to create these objects with `Author`.
    """

    class Meta:
        model = Author
        django_get_or_create = ("person",)

    quote = factory.Faker("sentence", nb_words=8, locale="ru_RU")
    biography = factory.Faker("text", locale="ru_RU")

    @factory.lazy_attribute
    def person(self):
        queryset = Person.objects.filter(email__isnull=False).exclude(city__exact="").exclude(image__exact="")
        person = queryset.order_by("?").first()
        return person

    @classmethod
    def _generate(cls, strategy, params):
        """Prevent to run factory if there is no required `Person` objects in db."""
        is_persons_with_email_city_image = (
            Person.objects.filter(email__isnull=False).exclude(city__exact="").exclude(image__exact="").exists()
        )
        assert is_persons_with_email_city_image, (
            "Create persons with with email, city and image before use that factory. The associated `Person` with "
            "`Author` has to have these fields filled in."
        )
        return super()._generate(strategy, params)

    @factory.post_generation
    def add_achievement(self, created: bool, count: int, **kwargs):
        """Create an Achievement object and link to self."""
        if not created:
            return
        if count:
            achievement_count = count
            achievements = AchievementFactory.create_batch(achievement_count)
            self.achievements.add(*achievements)

    @factory.post_generation
    def add_social_network_link(self, created: bool, count: int, **kwargs):
        """Create a SocialNetworkLink object and link to self."""
        if not created:
            return
        if count:
            links_count = count
            SocialNetworkLinkFactory.create_batch(links_count, author=self)

    @factory.post_generation
    def add_other_link(self, created: bool, count: int, **kwargs):
        """Create an OtherLink object and link to self."""
        if not created:
            return
        if count:
            links_count = count
            OtherLinkFactory.create_batch(links_count, author=self)

    @factory.post_generation
    def add_other_play(self, created: bool, count: int, **kwargs):
        """Create an OtherPlay object and link to self."""
        if not created:
            return
        if count:
            plays_count = count
            OtherPlayFactory.create_batch(plays_count, author=self)

    @factory.post_generation
    def plays(self, created: bool, extracted: Iterable[Play], **kwargs):
        """Add a Play objects to plays field for Author.

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
        """Create Author object with fully populated fields."""
        return cls.create(
            add_achievement=3,
            add_social_network_link=3,
            add_other_link=3,
            add_other_play=3,
            plays__num=3,
        )
