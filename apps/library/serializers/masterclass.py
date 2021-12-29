from rest_framework import serializers

from apps.library.models import MasterClass
from apps.library.utilities_team_data import team_data


class EventMasterClassSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()
    project_title = serializers.SlugRelatedField(slug_field="title", read_only=True, source="project")

    def get_team(self, obj):
        return team_data(obj, {"team_members__masterclass": obj, "slug__in": ["host"]})

    class Meta:
        model = MasterClass
        fields = (
            "id",
            "name",
            "description",
            "team",
            "project_title",
        )
