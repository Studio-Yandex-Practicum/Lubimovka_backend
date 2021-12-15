import factory
from faker import Faker

from apps.core.decorators import restrict_factory
from apps.core.models import Person, Role
from apps.core.tests.factories import RoleFactory
from apps.library.models import TeamMember

fake = Faker("ru_RU")


@restrict_factory({"global": [Person, Role]})
class TeamMemberFactory(factory.django.DjangoModelFactory):
    """
    Create TeamMember object.

    You should create at least one Person and Role
    before use this factory.
    This factory can be used only inside Reading, Performance
    or Master Class factories.
    """

    class Meta:
        model = TeamMember

    person = factory.Iterator(Person.objects.all())
    role = factory.SubFactory(RoleFactory)
