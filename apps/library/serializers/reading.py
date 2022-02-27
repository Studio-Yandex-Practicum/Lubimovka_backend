from typing import List

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.library.models import Reading
from apps.library.serializers.utilities import TeamTypedDict, get_event_team_roles, get_event_team_serialized_data


class EventReadingSerializer(serializers.ModelSerializer):
    """Сериализатор читки на странице афиши."""

    team = serializers.SerializerMethodField()
    project_title = serializers.SlugRelatedField(slug_field="title", read_only=True, source="project")

    @extend_schema_field(List[TeamTypedDict])
    def get_team(self, obj):
        """Собираем команду в два этапа.

        Сначала отбираем роли и связанные с ролью и событием персоны.
        Затем формируем словарь с правильной структурой.
        """
        roles = get_event_team_roles(obj, {"team_members__reading": obj, "slug__in": ["director", "dramatist"]})
        return get_event_team_serialized_data(roles)

    class Meta:
        model = Reading
        fields = (
            "id",
            "name",
            "description",
            "team",
            "project_title",
        )
