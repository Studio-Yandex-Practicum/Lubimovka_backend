import factory
from faker import Faker

from apps.core.decorators import restrict_factory
from apps.core.models import Person, Role
from apps.library.models import Play, Reading

from .team_member import TeamMemberFactory

fake = Faker("ru_RU")


@restrict_factory({"global": [Person, Play, Role]})
class ReadingFactory(factory.django.DjangoModelFactory):
    """
    Create Reading object.
    You should create at least one Play and Person and Role
    before use this factory.
    By default adds two team_members: dramatist and director
    For adding actors or other members use
    add_team_members=(actor, actor, text_adaptation, ...)
    """

    class Meta:
        model = Reading

    play = factory.Iterator(Play.objects.all())
    name = factory.LazyFunction(lambda: fake.word().capitalize())
    description = factory.Faker("text", locale="ru_RU")
    dramatist = factory.RelatedFactory(
        TeamMemberFactory,
        factory_related_name="reading",
        role__slug="dramatist",
    )
    director = factory.RelatedFactory(
        TeamMemberFactory,
        factory_related_name="reading",
        role__slug="director",
    )

    @factory.post_generation
    def add_team_members(self, created, extracted, **kwargs):
        if not created:
            return
        if extracted:
            roles = extracted
            for role in roles:
                self.team_members.add(
                    TeamMemberFactory(
                        reading=self,
                        role__slug=f"{role}",
                    )
                )
