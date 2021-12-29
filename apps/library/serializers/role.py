from rest_framework import serializers

from apps.core.models import Role

from .team_member import TeamMemberSerializer


class RoleSerializer(serializers.ModelSerializer):
    """Сериализатор для роли.

    Используется в сериализаторе спектакля,
    мастер-класса и читки на странице афиши,
    сериализаторе спектакля на странице отдельного спектакля.
    Применяется в случае, когда у роли только одна персона.
    """

    persons = TeamMemberSerializer(
        source="team_members",
        read_only=True,
        many=True,
    )

    class Meta:
        model = Role
        fields = (
            "name",
            "persons",
        )


class RoleWithPluralPersonsSerializer(serializers.ModelSerializer):
    """Сериализатор для роли.

    Используется в сериализаторе спектакля,
    мастер-класса и читки на странице афиши,
    сериализаторе спектакля на странице отдельного спектакля.
    Применяется в случае, когда у роли больше одной персоны.
    """

    name = serializers.CharField(source="name_plural")
    persons = TeamMemberSerializer(
        source="team_members",
        read_only=True,
        many=True,
    )

    class Meta:
        model = Role
        fields = (
            "name",
            "persons",
        )
