from typing import Iterable

import factory
from faker import Faker

from apps.articles.models import Project
from apps.core.decorators import restrict_factory
from apps.core.models import Person, Role
from apps.library.models import MasterClass

from .team_member import TeamMemberFactory

fake = Faker("ru_RU")


@restrict_factory({"global": (Person, Role), "add_project": (Project,)})
class MasterClassFactory(factory.django.DjangoModelFactory):
    """Create MasterClass object.

    !!! The `events` field (the name also confuses: actually it's
    OneToOneField) is created by a signal in afisha app.

    Parameters:
    1. `add_project`: links MasterClass with one of the existed `Project`.
    2. `add_team_members_with_roles`: waits for an iterable of strings. The
    strings should be a slug of any role. Selects random `Person` and add it to
    the `MasterClass` as team_member with the corresponding role.

    Not obvious details:
    1. `host_person`: it's not a model field. It's a `hook` to create `TeamMember`
    with "Ведущий" role.
    """

    class Meta:
        model = MasterClass

    class Params:
        add_project = factory.Trait(
            project=factory.LazyFunction(lambda: Project.objects.order_by("?").first()),
        )

    name = factory.LazyFunction(lambda: fake.word().capitalize())
    description = factory.Faker("text", locale="ru_RU")
    project = None

    host_person = factory.RelatedFactory(
        TeamMemberFactory,
        factory_related_name="masterclass",
        role__slug="host",
    )

    @factory.post_generation
    def add_team_members_with_roles(self, created, role_slugs: Iterable[str], **kwargs):
        """Add other team_members for created Reading object."""
        if not created:
            return
        if role_slugs:
            [TeamMemberFactory.create(reading=self, role_slug=role_slug) for role_slug in role_slugs]
