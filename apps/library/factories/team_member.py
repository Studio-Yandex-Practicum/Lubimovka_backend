import factory
from faker import Faker

from apps.core.decorators import restrict_factory
from apps.core.models import Person, Role, RoleType
from apps.library.models import TeamMember

fake = Faker("ru_RU")


@restrict_factory(general=(Person, Role))
class TeamMemberFactory(factory.django.DjangoModelFactory):
    """Create TeamMember object.

    The factory will fail if non of `performance` or `reading` or `masterclass`
    is set during call.

    You should create at least one Person and Role before use this factory.
    This factory can be used only inside Reading, Performance
    or Master Class factories.
    """

    class Meta:
        model = TeamMember
        django_get_or_create = (
            "person",
            "role",
            "performance",
            "reading",
            "masterclass",
        )

    performance = None
    reading = None
    masterclass = None

    @factory.lazy_attribute
    def person(self):
        return Person.objects.order_by("?").first()

    @factory.lazy_attribute
    def role(self):
        if self.performance:
            role_type = RoleType.objects.filter(role_type="performanse_role")
        if self.reading:
            role_type = RoleType.objects.filter(role_type="reading_role")
        if self.masterclass:
            role_type = RoleType.objects.filter(role_type="master_class_role")

        allowable_roles = Role.objects.filter(types__in=role_type)
        allowable_random_role = allowable_roles.order_by("?").first()
        return allowable_random_role
