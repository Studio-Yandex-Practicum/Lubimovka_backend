import pytest
from django.db import IntegrityError

from apps.core.factories import PersonFactory, RoleFactory
from apps.library.factories import MasterClassFactory, PerformanceFactory, ReadingFactory
from apps.library.models import TeamMember

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def some_role():
    return RoleFactory()


@pytest.fixture
def person_email_city_image():
    return PersonFactory(add_city=True, add_email=True, add_image=True)


@pytest.fixture
def masterclass_without_team_members():
    return MasterClassFactory(host_person=None)


@pytest.fixture
def reading_without_team_members(plays):
    return ReadingFactory(dramatist_person=None, director_person=None)


@pytest.fixture
def performance_without_team_members(plays):
    return PerformanceFactory(dramatist_person=None, director_person=None)


@pytest.mark.parametrize(
    "related_objects",
    (
        ("reading", "performance"),
        ("reading", "masterclass"),
        ("performance", "masterclass"),
    ),
)
def test_team_member_with_two_related_objects_raise_error(
    some_role,
    person_email_city_image,
    related_objects,
    masterclass_without_team_members,
    reading_without_team_members,
    performance_without_team_members,
):
    """Try to save `team_member` with two of performance, masterclass, reading and look for IntegrityError."""
    first_related_object_key = related_objects[0]
    second_related_object_key = related_objects[1]

    fixtures_mapping = {
        "reading": reading_without_team_members,
        "masterclass": masterclass_without_team_members,
        "performance": performance_without_team_members,
    }
    dict_to_create_team_member_with_one_related_object = {
        "person": person_email_city_image,
        "role": some_role,
        first_related_object_key: fixtures_mapping[first_related_object_key],
    }

    team_member = TeamMember.objects.create(**dict_to_create_team_member_with_one_related_object)
    with pytest.raises(IntegrityError):
        setattr(team_member, second_related_object_key, fixtures_mapping[second_related_object_key])
        team_member.save()
