import factory
from faker import Faker

from apps.core.decorators import restrict_factory
from apps.core.models import Person, Role
from apps.library.models import MasterClass

from .team_member import TeamMemberFactory

fake = Faker("ru_RU")


@restrict_factory({"global": [Person, Role]})
class MasterClassFactory(factory.django.DjangoModelFactory):
    """
    Create MasterClass object.

    You should create at least one Person and Role
    before use this factory.
    """

    class Meta:
        model = MasterClass

    name = factory.LazyFunction(lambda: fake.word().capitalize())
    description = factory.Faker("text", locale="ru_RU")
    member = factory.RelatedFactory(
        TeamMemberFactory,
        factory_related_name="masterclass",
        role__slug="host",
    )
