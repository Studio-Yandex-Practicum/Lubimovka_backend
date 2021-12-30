from rest_framework import serializers

from apps.core.models import Role


def team_persons(role):
    persons = []
    for team_member in role.team_members.all():
        persons.append(team_member.person.full_name)
    return persons


class RoleSerializer(serializers.ModelSerializer):
    """Сериализатор для роли.

    Используется в сериализаторе спектакля,
    мастер-класса и читки на странице афиши,
    сериализаторе спектакля на странице отдельного спектакля.
    Применяется в случае, когда у роли только одна персона.
    """

    persons = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = (
            "name",
            "persons",
        )

    def get_persons(self, obj):
        return team_persons(obj)


class RoleWithPluralPersonsSerializer(RoleSerializer):
    """Сериализатор для роли.

    Используется в сериализаторе спектакля,
    мастер-класса и читки на странице афиши,
    сериализаторе спектакля на странице отдельного спектакля.
    Применяется в случае, когда у роли больше одной персоны.
    """

    name = serializers.CharField(source="name_plural")
