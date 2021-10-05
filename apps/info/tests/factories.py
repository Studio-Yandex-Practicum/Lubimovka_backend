import urllib

import factory
from django.core.files.base import ContentFile
from faker import Faker

from apps.info.models import Partner

fake = Faker(["ru_Ru"])


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
