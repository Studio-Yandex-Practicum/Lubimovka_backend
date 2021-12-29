from rest_framework import serializers

from apps.core.models import Role

from .team_member import TeamMemberAfishaSerializer, TeamMemberSerializer


class RoleAfishaSerializer(serializers.ModelSerializer):
    """Сериализатор для роли.

    Используется в сериализаторе спектакля,
    мастер-класса и читки на странице афиши.
    """

    persons = TeamMemberAfishaSerializer(
        source="team_members",
        read_only=True,
        many=True,
    )

    class Meta:
        model = Role
        fields = (
            "name",
            "name_plural",
            "persons",
        )


class RoleSerializer(serializers.ModelSerializer):
    """Сериализатор для роли.

    Используется в сериализаторе
    спектакля на странице спектакля.
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
            "name_plural",
            "slug",
            "persons",
        )
