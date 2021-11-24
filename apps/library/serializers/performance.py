from rest_framework import serializers

from apps.core.serializers import ImageSerializer
from apps.library.models import Performance, TeamMember
from apps.library.utilities import team_collector

from .play import PlaySerializer


class PerformanceSerializer(serializers.ModelSerializer):
    """Сериализатор Спектакля для отображения на странице Спектакля"""

    play = PlaySerializer()
    persons = serializers.SerializerMethodField()
    images_in_block = ImageSerializer(many=True)

    def get_persons(self, obj):
        return team_collector(TeamMember, {"performance": obj})

    class Meta:
        exclude = (
            "created",
            "modified",
            "project",
        )
        model = Performance


class EventPerformanceSerializer(serializers.ModelSerializer):
    """Сериализатор Спектакля для отображения на странице Афиши"""

    team = serializers.SerializerMethodField()
    image = serializers.ImageField(source="main_image")
    project = serializers.SlugRelatedField(slug_field="title", read_only=True)

    def get_team(self, obj):
        return team_collector(
            TeamMember,
            {"performance": obj, "role__slug__in": ["director", "dramatist"]},
        )

    class Meta:
        model = Performance
        fields = (
            "id",
            "name",
            "description",
            "team",
            "image",
            "project",
        )
