from rest_framework import serializers

from apps.core.models import Role

from .team_member import TeamMemberSerializer


class RoleSerializer(serializers.ModelSerializer):
    """Сериализатор для роли.

    Используется в сериализаторе спектакля,
    мастер-класса и читки на странице афиши.
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

    Используется в сериализаторе
    спектакля на странице спектакля.
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
