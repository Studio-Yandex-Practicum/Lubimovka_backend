from django.db.models.query import Prefetch
from rest_framework import serializers

from apps.core.models import Role
from apps.library.models import MasterClass

from .role import RoleAfishaSerializer


class EventMasterClassSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()
    project_title = serializers.SlugRelatedField(slug_field="title", read_only=True, source="project")

    def get_team(self, obj):
        masterclass = obj
        masterclass_roles = Role.objects.filter(team_members__masterclass=masterclass, slug__in=("host",)).distinct()
        masterclass_team = masterclass.team_members.all()
        masterclass_roles_with_limited_persons = masterclass_roles.prefetch_related(
            Prefetch(
                "team_members",
                queryset=masterclass_team,
            ),
        )
        serializer = RoleAfishaSerializer(
            instance=masterclass_roles_with_limited_persons,
            many=True,
        )
        return serializer.data

    class Meta:
        model = MasterClass
        fields = (
            "id",
            "name",
            "description",
            "team",
            "project_title",
        )
