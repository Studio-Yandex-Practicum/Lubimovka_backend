from django.db.models.query import Prefetch

from apps.core.models import Role
from apps.library.serializers.role import RoleSerializer, RoleWithPluralPersonsSerializer


def get_event_team_roles(obj, filters: dict = None):
    """Получает все используемые в событии роли.

    С помощью Prefetch собирает связанные с ролью и событием персоны.
    """
    roles = Role.objects.filter(**filters).distinct()
    team = obj.team_members.all()
    return roles.prefetch_related(Prefetch("team_members", team))


def get_event_team_serialized_data(roles):
    """Формирует словарь со следующей структурой.

    [
      {
        "name": "Драматург",
        "persons": ["Антип Аксенова"]
        }
      ]
    В зависимости от количества персон у каждой роли
    используются разные сериализаторы.
    """
    data = []
    for role in roles:
        if role.team_members.count() == 1:
            serializer = RoleSerializer(instance=role)
        else:
            serializer = RoleWithPluralPersonsSerializer(instance=role)
        data.append(serializer.data)
    return data
