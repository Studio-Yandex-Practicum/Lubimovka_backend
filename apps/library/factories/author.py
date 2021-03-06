import factory
from faker import Faker

from apps.core import utils
from apps.core.decorators import restrict_factory
from apps.core.models import Person
from apps.info.models import Festival
from apps.info.utils import get_random_objects_by_model, get_random_objects_by_queryset
from apps.library.models import Author, OtherLink, ProgramType, SocialNetworkLink

fake = Faker("ru_RU")


@restrict_factory(general=(Author,))
class SocialNetworkLinkFactory(factory.django.DjangoModelFactory):
    """Create SocialNetworkLink object."""

    class Meta:
        model = SocialNetworkLink
        django_get_or_create = ("author", "name")

    name = factory.Iterator(SocialNetworkLink.SocialNetwork.values)
    link = factory.Faker("url")

    @factory.lazy_attribute
    def author(self):
        return get_random_objects_by_model(Author)


@restrict_factory(general=(Author,))
class OtherLinkFactory(factory.django.DjangoModelFactory):
    """Create OtherLink object."""

    class Meta:
        model = OtherLink
        django_get_or_create = ("author", "name")

    name = factory.LazyFunction(lambda: fake["ru_RU"].word().capitalize())
    link = factory.Faker("url")
    is_pinned = factory.Faker("pybool")

    @factory.lazy_attribute
    def author(self):
        return get_random_objects_by_queryset(Author.objects.all())


@restrict_factory(general=(Person, Festival, ProgramType))
class AuthorFactory(factory.django.DjangoModelFactory):
    """Create Author object.

    Parameters:
    1. `add_several_achievement`: create <int> `Achievement` objects, link to `Author`.
    2. `add_several_social_network_link`:  create <int> `SocialNetworkLink` objects, link to `Author`.
    3. `add_several_other_link`: create <int> `OtherLink` objects, link to `Author`.

    Class methods:
    1. `complex_create`:  shortcut. Create `Author` with fully populated fields.

    The fields `city`, `email`, `image` has to be filled in the `Person` object.
    Otherwise, it should not be associated with the `Author`.

    Author object is linked to `Achievement`, `SocialNetworkLink`, `OtherLink`,
    objects with m2m connection. These models aren't used elsewhere.
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
        person = get_random_objects_by_queryset(queryset)
        return person

    @factory.lazy_attribute
    def slug(self):
        full_name = self.person.first_name + "_" + self.person.last_name
        slug = utils.slugify(full_name)
        return slug

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

    @classmethod
    def complex_create(cls, count=1):
        """Create Author object with fully populated fields."""
        return cls.create_batch(
            count,
            add_social_network_link=3,
            add_other_link=3,
        )
