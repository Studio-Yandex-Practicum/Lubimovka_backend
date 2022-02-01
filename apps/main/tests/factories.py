import urllib

import factory
from django.core.files.base import ContentFile

from ..models import Banner


class BannerFactory(factory.django.DjangoModelFactory):
    """Main banner factory.

    No more than 3 banner objects could be created. The factory couldn't be
    used to update existed objects.
    """

    class Meta:
        model = Banner
        django_get_or_create = ("id",)

    id = factory.Iterator(range(3))
    title = factory.Faker("sentence", nb_words=6, locale="ru_RU")
    description = factory.Faker("sentence", nb_words=16, locale="ru_RU")
    url = factory.Faker("url")
    image = factory.django.ImageField(color=factory.Faker("color"))
    button = factory.Iterator(Banner.ButtonType.values)

    @factory.post_generation
    def add_real_image(self, created, extracted, **kwargs):
        """Set image from picsum.photos. Requires internet connection.

        To use it set `add_real_image=True`
        """
        if extracted is True:
            image = urllib.request.urlopen("https://picsum.photos/800/800").read()
            self.image.save(self.title + ".jpg", ContentFile(image), save=False)
