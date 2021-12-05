import random
import urllib

import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files.base import ContentFile
from faker import Faker

from apps.core.models import Image, Person
from apps.core.utilities import slugify

fake = Faker(locale="ru_RU")

User = get_user_model()


class PersonFactory(factory.django.DjangoModelFactory):
    """
    Creates Person objects.
    In default creates: first_name, last_name, middle_name.
    For other fields, use arguments: add_email, add_city, add_image.
    """

    class Meta:
        model = Person

    first_name = factory.Faker("first_name", locale="ru_RU")
    last_name = factory.Faker("last_name", locale="ru_RU")
    middle_name = factory.Faker("middle_name", locale="ru_RU")

    @factory.post_generation
    def add_email(self, created, extracted, **kwargs):
        """
        Add Email field for Person (needs for volunteers, teams)
        To use "add_email=True"
        """
        if not created:
            return

        if extracted:
            self.email = (
                slugify(self.first_name + self.last_name) + "@lubimovka.ru"
            )

    @factory.post_generation
    def add_city(self, created, extracted, **kwargs):
        """
        Add City field for Person (needs for volunteers, teams)
        To use "add_city=True"
        """
        if not created:
            return

        if extracted:
            self.city = fake.city_name()

    @factory.post_generation
    def add_image(self, created, extracted, **kwargs):
        """
        Add Image field for Person
        To use "add_image=True"
        """
        if not created:
            return

        if extracted:
            image = urllib.request.urlopen(
                "https://picsum.photos/210/265"
            ).read()
            self.image.save(
                self.first_name + " " + self.last_name + ".jpg",
                ContentFile(image),
                save=False,
            )


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image
        django_get_or_create = ("image",)

    image = factory.django.ImageField(
        color=factory.LazyFunction(
            lambda: random.choice(["blue", "yellow", "green", "orange"])
        ),
        width=factory.LazyFunction(lambda: random.randint(10, 1000)),
        height=factory.SelfAttribute("width"),
    )


class UserFactory(factory.django.DjangoModelFactory):
    """
    Creates User objects.
    Creates username and default password.
    For other fields, use arguments: add_role_editor, add_role_admin.
    """

    class Meta:
        model = User

    username = factory.Faker("user_name")
    password = factory.PostGenerationMethodCall("set_password", "pass")

    @factory.post_generation
    def add_role_editor(self, created, extracted, **kwargs):
        """
        Add role Editor to User.
        To use "add_role_editor=True"
        """
        if not created:
            return

        if extracted:
            group = Group.objects.get(name="editor")
            self.groups.add(group)

    @factory.post_generation
    def add_role_admin(self, created, extracted, **kwargs):
        """
        Add role Admin to User.
        To use "add_role_admin=True"
        """
        if not created:
            return

        if extracted:
            group = Group.objects.get(name="admin")
            self.groups.add(group)
