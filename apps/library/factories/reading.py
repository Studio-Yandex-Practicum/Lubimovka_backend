from typing import Iterable

import factory
from faker import Faker

from apps.core.decorators import restrict_factory
from apps.core.models import Person, Role
from apps.library.models import Play, Reading

from .team_member import TeamMemberFactory

fake = Faker("ru_RU")


@restrict_factory(general=(Person, Play, Role))
class ReadingFactory(factory.django.DjangoModelFactory):
    """Create Reading object.

    !!! The `events` field (the name also confuses: actually it's
    OneToOneField) is created by a signal in afisha app.

    Parameters:
    - `add_team_members_with_roles`: waits for an iterable of strings. The
    strings should be a slug of any role. Selects random `Person` and add it to
    the `Reading` as team_member with the corresponding role.

    Not obvious details:
    - `dramatist_person` and `director_person`: it's not a model fields. It's a
    `hook`s to create `TeamMember` with roles "Драматург" and "Режиссер".
    """

    class Meta:
        model = Reading

    name = factory.LazyFunction(lambda: fake.word().capitalize())
    description = factory.Faker("text", locale="ru_RU")

    @factory.lazy_attribute
    def play(self):
        return Play.objects.filter(other_play=False).order_by("?").first()

    dramatist_person = factory.RelatedFactory(
        TeamMemberFactory,
        factory_related_name="reading",
        set_role_with_slug="dramatist",
    )
    director_person = factory.RelatedFactory(
        TeamMemberFactory,
        factory_related_name="reading",
        set_role_with_slug="director",
    )

    @factory.post_generation
    def add_team_members_with_roles(self, created, role_slugs: Iterable[str], **kwargs):
        """Add other team_members for created Reading object."""
        if not created:
            return
        if role_slugs:
            [TeamMemberFactory.create(reading=self, role_slug=role_slug) for role_slug in role_slugs]
