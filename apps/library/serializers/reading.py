from django.db.models.query import Prefetch
from rest_framework import serializers

from apps.core.models import Role
from apps.library.models import Reading

from .role import RoleSerializer


class EventReadingSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()
    project_title = serializers.SlugRelatedField(slug_field="title", read_only=True, source="project")

    def get_team(self, obj):
        reading = obj
        reading_roles = Role.objects.filter(
            team_members__reading=reading, slug__in=("director", "dramatist")
        ).distinct()
        reading_team = reading.team_members.all()
        reading_roles_with_limited_persons = reading_roles.prefetch_related(
            Prefetch(
                "team_members",
                queryset=reading_team,
            ),
        )
        serializer = RoleSerializer(
            instance=reading_roles_with_limited_persons,
            many=True,
        )
        return serializer.data

    class Meta:
        model = Reading
        fields = (
            "id",
            "name",
            "description",
            "team",
            "project_title",
        )
