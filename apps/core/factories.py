import factory
from django.db import models
from faker import Faker

from apps.core.decorators import restrict_factory
from apps.core.models import Image, Person, Role, RoleType
from apps.core.utils import get_picsum_image, slugify

fake = Faker(locale="ru_RU")


class PersonFactory(factory.django.DjangoModelFactory):
    """Create Person objects.

    Parameters:
    1. `add_image`: create Person with fake not empty image
    2. `add_real_image`: create Person with real image. Requires internet.
    3. `add_city`: create Person with fake not empty city
    4. `add_email`: create Person with fake email link nikolaykiryanov@lubimovka.ru
    """

    class Meta:
        model = Person

    first_name = factory.Faker("first_name", locale="ru_RU")
    last_name = factory.Faker("last_name", locale="ru_RU")
    middle_name = factory.Faker("middle_name", locale="ru_RU")
    email = None
    image = ""
    city = ""

    class Params:
        add_image = factory.Trait(
            image=factory.django.ImageField(color=factory.Faker("color")),
        )
        add_real_image = factory.Trait(
            image=factory.django.ImageField(from_func=get_picsum_image),
        )
        add_city = factory.Trait(
            city=factory.Faker("city_name", locale="ru_RU"),
        )
        add_email = factory.Trait(
            email=factory.LazyAttributeSequence(
                lambda person, index: f"{slugify(person.first_name + person.last_name)}_{index:02d}@lubimovka.ru"
            ),
        )


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image
        django_get_or_create = ("image",)

    image = factory.django.ImageField(
        color=factory.Faker("color"),
        width=factory.Faker("random_int", min=10, max=1000),
        height=factory.SelfAttribute("width"),
    )


class RoleTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RoleType
        django_get_or_create = ("role_type",)

    role_type = factory.Iterator(RoleType.SelectRoleType.values)


class RoleFactoryData(models.TextChoices):
    """DjangoEnum class is used to store slug, name, name_plural for RoleFactory.

    Mapping:
        - RoleFactoryData.names: returns role's slugs
        - RoleFactoryData.values: returns role's names
        - RoleFactoryData.labels: returns role's plural_names

    The class extended with two properties for convenience:
        - RoleFactoryData.slug: returns role's slug
        - RoleFactoryData.name_plural: returns role's name_plural
    """

    actor = "Актёр", "Актеры"
    author = "Автор", "Авторы"
    director = "Режиссёр", "Режиссёры"
    dramatist = "Драматург", "Драматурги"
    host = "Ведущий", "Ведущие"
    illustrations = "Иллюстрации", "Иллюстрации"
    photo = "Фото", "Фото"
    text_adaptation = "Адаптация текста", "Адаптация текста"
    translator = "Переводчик", "Переводчики"
    text = "Текст", "Текст"

    @property
    def slug(self):
        return self.name

    @property
    def name_plural(self):
        return self.label


@restrict_factory(general=(RoleType,))
class RoleFactory(factory.django.DjangoModelFactory):
    """Create roles based on RoleFactoryData and set at least one role_type.

    Parameters:
    1. `role_type`: wait for `role_type` text name and set it to the role.
    Example: `role_type="blog_persons_role"`,
    """

    class Meta:
        model = Role
        django_get_or_create = ("slug",)

    name = factory.Iterator(iterator=RoleFactoryData.values)

    @factory.lazy_attribute
    def slug(self):
        slug = RoleFactoryData(self.name).slug
        return slug

    @factory.lazy_attribute
    def name_plural(self):
        name_plural = RoleFactoryData(self.name).name_plural
        return name_plural

    @factory.post_generation
    def role_type(self, create, role_type, **kwargs):
        if create and role_type:
            assert type(role_type) is str, "Тип роли должны быть строкой."
            role_type = RoleType.objects.filter(role_type=role_type)
            self.types.set(role_type)
