from rest_framework import serializers

from apps.library.models import MasterClass
from apps.library.serializers.utilities import get_roles, get_serialized_data


class EventMasterClassSerializer(serializers.ModelSerializer):
    """Сериализатор мастер-класса на странице афиши."""

    team = serializers.SerializerMethodField()
    project_title = serializers.SlugRelatedField(slug_field="title", read_only=True, source="project")

    def get_team(self, obj):
        """Собираем команду в два этапа.

        Сначала отбираем роли и связанные с ролью и событием персоны.
        Затем формируем словарь с правильной структурой.
        """
        roles = get_roles(obj, {"team_members__masterclass": obj, "slug__in": ["host"]})
        return get_serialized_data(roles)

    class Meta:
        model = MasterClass
        fields = (
            "id",
            "name",
            "description",
            "team",
            "project_title",
        )
