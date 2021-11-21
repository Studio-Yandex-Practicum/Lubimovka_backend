from rest_framework import serializers

from apps.library.models import TeamMember


class TeamMemberSerializer(serializers.ModelSerializer):
    """Сериализатор промежуточной модели Команда спектакля
    для вложения в сериализатор Спектакля"""

    name = serializers.ReadOnlyField(source="person.full_name")
    role = serializers.ReadOnlyField(source="role.name")

    class Meta:
        fields = (
            "role",
            "name",
        )
        model = TeamMember
