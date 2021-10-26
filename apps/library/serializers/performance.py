from rest_framework import serializers

from apps.core.serializers import ImageSerializer
from apps.library.models import Performance

from .performanceperson import PerformancePersonSerializer
from .play import PlaySerializer


class PerformanceSerializer(serializers.ModelSerializer):
    """Сериализатор Спектакля для отображения на странице Спектакля"""

    play = PlaySerializer()
    persons = PerformancePersonSerializer(
        source="performance_persons",
        many=True,
    )
    images_in_block = ImageSerializer(many=True)

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
