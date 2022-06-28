import random

import factory
from faker import Faker

from apps.core.decorators import restrict_factory
from apps.core.models import Person
from apps.core.utils import get_picsum_image
from apps.info.models import (
    Festival,
    FestivalImage,
    FestivalTeamMember,
    InfoLink,
    Partner,
    Place,
    PressRelease,
    Selector,
    Sponsor,
    Volunteer,
)
from apps.info.utils import get_random_objects_by_model, get_random_objects_by_queryset
from apps.library.factories.constants import YOUTUBE_VIDEO_LINKS

fake = Faker(locale="en_US")


class PartnerFactory(factory.django.DjangoModelFactory):
    """Create Partner objects.

    The behavior is different based on param:
        - `add_real_image`: create Partner with real image. Requires internet.
    """

    class Meta:
        model = Partner
        django_get_or_create = ("name",)

    class Params:
        add_real_image = factory.Trait(
            image=factory.django.ImageField(from_func=get_picsum_image),
        )

    name = factory.Faker("company", locale="ru_RU")
    type = factory.Iterator(Partner.PartnerType.values)
    url = factory.Faker("url", locale="ru_RU")
    image = factory.django.ImageField(color=factory.Faker("color"))
    in_footer_partner = False


class SponsorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sponsor
        django_get_or_create = ("person",)

    position = factory.Faker("job", locale="ru_RU")

    @factory.lazy_attribute
    def person(self):
        queryset = Person.objects.filter(city__exact="").exclude(image__exact="")
        person = get_random_objects_by_queryset(queryset)
        return person


@restrict_factory(general=(Festival, Person))
class VolunteerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Volunteer
        django_get_or_create = ("person", "festival")

    festival = factory.LazyFunction(lambda: get_random_objects_by_model(Festival))
    review_title = factory.Faker("text", max_nb_chars=50, locale="ru_RU")
    review_text = factory.Faker("text", max_nb_chars=1000, locale="ru_RU")

    @factory.lazy_attribute
    def person(self):
        queryset = Person.objects.filter(email__isnull=False).exclude(image__exact="")
        person = get_random_objects_by_queryset(queryset)
        return person


@restrict_factory(general=(Festival, Person))
class SelectorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Selector
        django_get_or_create = ("person", "festival")

    festival = factory.LazyFunction(lambda: get_random_objects_by_queryset(Festival.objects.all()))
    position = factory.Faker("job", locale="ru_RU")

    @factory.lazy_attribute
    def person(self):
        queryset = Person.objects.filter(email__isnull=False).exclude(image__exact="")
        person = get_random_objects_by_queryset(queryset)
        return person


@restrict_factory(general=(Person,))
class FestivalTeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FestivalTeamMember
        django_get_or_create = ("person", "team")

    team = factory.Iterator(FestivalTeamMember.TeamType.values)
    position = factory.Faker("job", locale="ru_RU")
    is_pr_director = False

    @factory.lazy_attribute
    def person(self):
        queryset = Person.objects.filter(city__isnull=False, email__isnull=False).exclude(image__exact="")
        person = get_random_objects_by_queryset(queryset)
        return person


class FestivalFactory(factory.django.DjangoModelFactory):
    """Create Festival object with 1-6 images."""

    class Meta:
        model = Festival
        django_get_or_create = ("year",)

    start_date = factory.Faker("past_date")
    end_date = factory.Faker("future_date")
    description = factory.Faker("sentence", locale="ru_RU")
    year = factory.Faker("random_int", min=1990, max=2022, step=1)

    @factory.post_generation
    def images(self, create, extracted, **kwargs):
        if create:
            images_count = random.randint(1, 6)
            FestivalImageFactory.create_batch(images_count, festival=self)

    @factory.post_generation
    def infolinks(self, create, extracted, **kwargs):
        if create:
            links_count = random.randint(2, 9)
            InfoLinkFactory.create_batch(links_count, festival=self)

    plays_count = factory.Faker("random_int", min=20, max=200, step=1)
    selected_plays_count = factory.Faker("random_int", min=1, max=20, step=1)
    selectors_count = factory.Faker("random_int", min=1, max=20, step=1)
    volunteers_count = factory.Faker("random_int", min=1, max=20, step=1)
    events_count = factory.Faker("random_int", min=1, max=20, step=1)
    cities_count = factory.Faker("random_int", min=1, max=20, step=1)
    video_link = factory.LazyFunction(lambda: random.choice(YOUTUBE_VIDEO_LINKS))
    # blog_entries необходимо изменить после
    # корректировки поля модели фестиваля
    blog_entries = factory.LazyFunction(lambda: fake.word(ext_word_list=["abc", "def", "ghi", "jkl"]))
    festival_image = factory.django.ImageField(color=factory.Faker("color"))


@restrict_factory(general=(Festival,))
class FestivalImageFactory(factory.django.DjangoModelFactory):
    """Create Images for Festival."""

    class Meta:
        model = FestivalImage
        django_get_or_create = ("image",)

    image = factory.django.ImageField(
        color=factory.Faker("color"),
        width=factory.Faker("random_int", min=10, max=1000),
        height=factory.SelfAttribute("width"),
    )

    @factory.lazy_attribute
    def festival(self):
        return get_random_objects_by_model(Festival)


@restrict_factory(general=(Festival,))
class InfoLinkFactory(factory.django.DjangoModelFactory):
    """Create other InfoLinks for Festival."""

    class Meta:
        model = InfoLink

    type = factory.Iterator(InfoLink.LinkType.values)
    title = factory.Faker("sentence", locale="ru_RU")
    link = factory.Faker("url")

    @factory.lazy_attribute
    def festival(self):
        return get_random_objects_by_model(Festival)


@restrict_factory(general=(Festival,))
class PressReleaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PressRelease
        django_get_or_create = ("festival",)

    title = factory.Faker("sentence", locale="ru_RU")
    text = factory.Faker("text", locale="ru_RU")
    press_release_image = factory.django.ImageField(color=factory.Faker("color"))

    @factory.lazy_attribute
    def festival(self):
        return get_random_objects_by_model(Festival)


class PlaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Place
        django_get_or_create = ("name", "city")

    name = factory.Faker("word", locale="ru_RU")
    description = factory.Faker("sentence", locale="ru_RU")
    city = factory.Faker("city", locale="ru_RU")
    address = factory.Faker("street_address", locale="ru_RU")
    map_link = factory.Faker("url", locale="ru_RU")
