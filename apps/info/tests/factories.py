import urllib

import factory
from django.core.files.base import ContentFile

from apps.core.models import Person
from apps.info.models import FestivalTeam, Partner, Sponsor, Volunteer


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

    person = factory.Iterator(
        Person.objects.filter(city__exact="").exclude(image__exact="")
    )
    position = factory.Faker("job", locale="ru_RU")


class VolunteerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Volunteer
        django_get_or_create = ["person"]

    person = person = factory.Iterator(
        Person.objects.filter(email__isnull=False).exclude(image__exact="")
    )
    year = factory.Faker("random_int", min=2018, max=2021, step=1)
    review = factory.Faker("text", max_nb_chars=1000, locale="ru_RU")


class FestivalTeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FestivalTeam
        django_get_or_create = ["person", "team"]

    person = factory.Iterator(
        Person.objects.filter(city__isnull=False, email__isnull=False).exclude(
            image__exact=""
        )
    )
    team = factory.Iterator(
        FestivalTeam.TeamType.choices,
        getter=lambda choice: choice[0],
    )
    position = factory.Faker("job", locale="ru_RU")
