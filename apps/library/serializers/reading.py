from rest_framework import serializers

from apps.library.models import Reading, TeamMember


class EventReadingSerializer(serializers.ModelSerializer):
    directors = serializers.SerializerMethodField()
    dramatists = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()

    def get_directors(self, obj):
        directors = TeamMember.objects.filter(
            reading=obj, role__name="Режиссёр"
        )
        return [director.person.full_name for director in directors]

    def get_dramatists(self, obj):
        dramatists = TeamMember.objects.filter(
            reading=obj, role__name="Драматург"
        )
        return [dramatist.person.full_name for dramatist in dramatists]

    def get_project(self, obj):
        if obj.project:
            return obj.project.title
        return ""

    class Meta:
        model = Reading
        fields = (
            "id",
            "name",
            "description",
            "directors",
            "dramatists",
            "project",
        )
