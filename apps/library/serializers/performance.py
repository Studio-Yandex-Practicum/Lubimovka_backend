from rest_framework import serializers

from apps.core.serializers import ImagesInBlockInPerformanceSerializer
from apps.library.models import Performance

from .performanceteam import PerformanceTeamSerializer
from .play import PlayInPerformanceSerializer


class PerformanceSerializer(serializers.ModelSerializer):
    """Сериализатор Спектакля для отображения на странице Спектакля"""

    play = PlayInPerformanceSerializer()
    team_members = PerformanceTeamSerializer(
        source="performanceteam_set",
        many=True,
    )
    images_in_block = ImagesInBlockInPerformanceSerializer(many=True)

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
