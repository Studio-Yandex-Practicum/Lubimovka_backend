from rest_framework import serializers

from apps.library.models import PerformancePerson


class PerformancePersonSerializer(serializers.ModelSerializer):
    """Сериализатор промежуточной модели Команда спектакля
    для вложения в сериализатор Спектакля"""

    name = serializers.ReadOnlyField(source="person.full_name")

    class Meta:
        fields = ["role", "name"]
        model = PerformancePerson
