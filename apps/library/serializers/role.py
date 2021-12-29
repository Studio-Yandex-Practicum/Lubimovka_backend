from rest_framework import serializers

from apps.core.models import Role

from .team_member import TeamMemberSerializer


class RoleSerializer(serializers.ModelSerializer):
    """Сериализатор для роли.

    Используется в сериализаторе
    спектакля на странице спектакля и в сериализаторе спектакля,
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
            "name_plural",
            "slug",
            "persons",
        )
