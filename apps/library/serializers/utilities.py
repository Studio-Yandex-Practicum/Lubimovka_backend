from django.db.models.query import Prefetch

from apps.core.models import Role
from apps.library.serializers.role import RoleSerializer, RoleWithPluralPersonsSerializer


def team_data(obj, filters: dict = None):
    """Group team members by roles.

    Form array with next structure:
    [
      {
        "name": "Драматурги",
          "persons": [
            {"full_name": "Наум Быкова"},
            {"full_name": "Анатолий Соболева"}
                      ]
        },
      {
        "name": "Режиссёр",
        "persons": [
          {"full_name": "Рубен Васильева"}
                    ]
        }
      ]
    Duplication of role, name pairs should be avoided by model's constraints.
    """
    roles = Role.objects.filter(**filters).distinct()
    team = obj.team_members.all()
    roles_with_limited_persons = roles.prefetch_related(Prefetch("team_members", team))
    data = []
    for role in roles_with_limited_persons:
        if role.team_members.count() == 1:
            serializer = RoleSerializer(instance=role)
        else:
            serializer = RoleWithPluralPersonsSerializer(instance=role)
        data.append(serializer.data)
    return data
