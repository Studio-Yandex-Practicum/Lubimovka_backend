import factory

from apps.core.utils import get_random_image
from apps.main.models import Banner


class BannerFactory(factory.django.DjangoModelFactory):
    """Main banner factory.

    No more than 3 banner objects could be created. The factory couldn't be
    used to update existed objects.

    Parameters:
    1. `add_real_image`: create Banner with real image. Requires internet.
    """

    class Meta:
        model = Banner
        django_get_or_create = ("id",)

    class Params:
        add_real_image = factory.Trait(
            image=factory.django.ImageField(from_func=get_random_image),
        )

    id = factory.Iterator(range(1, 4))
    title = factory.Faker("sentence", nb_words=6, locale="ru_RU")
    description = factory.Faker("sentence", nb_words=16, locale="ru_RU")
    url = factory.Faker("url")
    image = factory.django.ImageField(color=factory.Faker("color"))
    button = factory.Iterator(Banner.ButtonType.values)
