from rest_framework import serializers

from apps.core.serializers import ImageSerializer
from apps.library.models import Performance, TeamMember

from .performanceperson import TeamMemberSerializer
from .play import PlaySerializer


class PerformanceSerializer(serializers.ModelSerializer):
    """Сериализатор Спектакля для отображения на странице Спектакля"""

    play = PlaySerializer()
    persons = TeamMemberSerializer(
        source="team_members",
        many=True,
    )
    images_in_block = ImageSerializer(many=True)

    class Meta:
        exclude = (
            "created",
            "modified",
        )
        model = Performance


class EventPerformanceSerializer(serializers.ModelSerializer):
    """Сериализатор Спектакля для отображения на странице Афиши"""

    directors = serializers.SerializerMethodField()
    dramatists = serializers.SerializerMethodField()
    image = serializers.ImageField(source="main_image")
    project = serializers.SerializerMethodField()

    def get_directors(self, obj):
        directors = TeamMember.objects.filter(
            performance=obj, role__name="Режиссёр"
        )
        return [director.person.full_name for director in directors]

    def get_dramatists(self, obj):
        dramatists = TeamMember.objects.filter(
            performance=obj, role__name="Драматург"
        )
        return [dramatist.person.full_name for dramatist in dramatists]

    def get_project(self, obj):
        if obj.project:
            return obj.project.title
        return ""

    class Meta:
        model = Performance
        fields = (
            "id",
            "name",
            "description",
            "directors",
            "dramatists",
            "image",
            "project",
        )
