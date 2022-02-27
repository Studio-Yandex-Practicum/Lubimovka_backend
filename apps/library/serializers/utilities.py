from typing import List, TypedDict

from django.db.models.query import Prefetch

from apps.core.models import Role
from apps.library.serializers.role import RoleSerializer, RoleWithPluralPersonsSerializer


class TeamTypedDict(TypedDict):
    """Type hint for 'team' field in PerformanceSerializer."""

    name: str
    persons: List[str]


def get_event_team_roles(obj, filters: dict = None):
    """Return all roles used in event.

    Collects persons related with role using Prefetch.
    """
    roles = Role.objects.filter(**filters).distinct()
    team = obj.team_members.all()
    return roles.prefetch_related(Prefetch("team_members", team))


def get_event_team_serialized_data(roles) -> List[TeamTypedDict]:
    """Return list of dictionary with next structure.

    [
      {
        "name": "Драматург",
        "persons": ["Антип Аксенова"]
        }
      ]
    Which serializer will be used depends on person's number of each role.
    """
    data = []
    for role in roles:
        if role.team_members.count() == 1:
            serializer = RoleSerializer(instance=role)
        else:
            serializer = RoleWithPluralPersonsSerializer(instance=role)
        data.append(serializer.data)
    return data
