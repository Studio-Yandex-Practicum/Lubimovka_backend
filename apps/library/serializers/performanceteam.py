from rest_framework import serializers

from apps.library.models import PerformanceTeam


class PerformanceTeamSerializer(serializers.ModelSerializer):
    """Сериализатор промежуточной модели Команда спектакля
    для вложения в сериализатор Спектакля"""

    member = serializers.ReadOnlyField(source="member.full_name")

    class Meta:
        fields = ("role", "member")
        model = PerformanceTeam
