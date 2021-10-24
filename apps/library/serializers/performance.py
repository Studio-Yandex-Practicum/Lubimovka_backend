from rest_framework import serializers

from apps.core.serializers import PerformanceImagesBlockSerializer
from apps.library.models import Performance

from .performanceteam import PerformanceTeamSerializer
from .play import PlaySerializer


class PerformanceSerializer(serializers.ModelSerializer):
    """Сериализатор Спектакля для отображения на странице Спектакля"""

    play = PlaySerializer()
    members = PerformanceTeamSerializer(
        source="members_set",
        many=True,
    )
    images_in_block = PerformanceImagesBlockSerializer(many=True)

    class Meta:
        exclude = [
            "created",
            "modified",
        ]
        model = Performance


class PerformanceEventSerializer(serializers.ModelSerializer):
    """Сериализатор Спектакля для отображения на странице Афиши"""

    class Meta:
        model = Performance
        fields = ["id", "name", "description"]
