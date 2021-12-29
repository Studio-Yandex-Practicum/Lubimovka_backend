from rest_framework import serializers

from apps.library.models import TeamMember


class TeamMemberSerializer(serializers.ModelSerializer):
    """Сериализатор для членов команды.

    Используется в сериализаторе роли.
    """

    id = serializers.SlugRelatedField(
        source="person",
        slug_field="id",
        read_only=True,
    )
    full_name = serializers.SlugRelatedField(
        source="person",
        slug_field="full_name",
        read_only=True,
    )

    class Meta:
        model = TeamMember
        fields = (
            "id",
            "full_name",
        )
