import random
import urllib

import factory
from django.core.files.base import ContentFile
from faker import Faker

from apps.core.decorators import restrict_factory
from apps.core.models import Image, Person
from apps.info.models import Festival, FestivalTeam, Partner, PressRelease, Sponsor, Volunteer

fake = Faker(locale="en_US")


class PartnerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Partner
        django_get_or_create = ["name"]

    name = factory.Faker("company", locale="ru_RU")
    type = factory.Iterator(
        Partner.PartnerType.choices,
        getter=lambda choice: choice[0],
    )
    url = factory.Faker("url", locale="ru_RU")
    in_footer_partner = False

    @factory.post_generation
    def image(self, created, extracted, **kwargs):
        if not created:
            return

        image = urllib.request.urlopen("https://placeimg.com/200/100").read()
        self.image.save(self.name + ".jpg", ContentFile(image), save=False)


class SponsorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sponsor
        django_get_or_create = ["person"]

    person = factory.Iterator(Person.objects.filter(city__exact="").exclude(image__exact=""))
    position = factory.Faker("job", locale="ru_RU")


@restrict_factory({"global": [Festival, Person]})
class VolunteerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Volunteer
        django_get_or_create = ["person"]
        django_get_or_create = ("festival",)

    festival = factory.Iterator(Festival.objects.all())
    person = factory.Iterator(Person.objects.filter(email__isnull=False).exclude(image__exact=""))
    review_title = factory.Faker("text", max_nb_chars=50, locale="ru_RU")
    review_text = factory.Faker("text", max_nb_chars=1000, locale="ru_RU")


class FestivalTeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FestivalTeam
        django_get_or_create = ["person", "team"]

    person = factory.Iterator(Person.objects.filter(city__isnull=False, email__isnull=False).exclude(image__exact=""))
    team = factory.Iterator(
        FestivalTeam.TeamType.choices,
        getter=lambda choice: choice[0],
    )
    position = factory.Faker("job", locale="ru_RU")


class FestivalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Festival
        django_get_or_create = ("year",)

    start_date = factory.Faker("past_date")
    end_date = factory.Faker("future_date")
    description = factory.Faker("sentence", locale="ru_RU")
    year = factory.Faker("random_int", min=1990, max=2021, step=1)

    @factory.post_generation
    def images(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.images.add(*extracted)
        else:
            images_count = Image.objects.count()
            how_many = min(images_count, random.randint(1, 7))
            images = Image.objects.order_by("?")[:how_many]
            self.images.add(*images)

    plays_count = factory.Faker("random_int", min=20, max=200, step=1)
    selected_plays_count = factory.Faker("random_int", min=1, max=20, step=1)
    selectors_count = factory.Faker("random_int", min=1, max=20, step=1)
    volunteers_count = factory.Faker("random_int", min=1, max=20, step=1)
    events_count = factory.Faker("random_int", min=1, max=20, step=1)
    cities_count = factory.Faker("random_int", min=1, max=20, step=1)
    video_link = factory.Faker("url", locale="ru_RU")
    # blog_entries необходимо изменить после
    # корректировки поля модели фестиваля
    blog_entries = factory.LazyFunction(lambda: fake.word(ext_word_list=["abc", "def", "ghi", "jkl"]))
    press_release_image = factory.django.ImageField(color="blue")


@restrict_factory({"global": [Festival]})
class PressReleaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PressRelease
        django_get_or_create = ("festival",)

    festival = factory.Iterator(Festival.objects.all())
    title = factory.Faker("sentence", locale="ru_RU")
    text = factory.Faker("text", locale="ru_RU")
