from typing import Optional

from rest_framework import serializers

from apps.afisha.models import Event, Performance, Reading
from apps.afisha.serializers import EventPerformanceSerializer, EventReadingSerializer
from apps.library.serializers.role import RoleSerializer

AFISHA_EVENTS_SERIALIZER_PAIRS = {
    Performance: EventPerformanceSerializer,
    Reading: EventReadingSerializer,
}


class BaseEventSerializer(serializers.ModelSerializer):
    """Base event info for afisha and content blocks."""

    more_info_type = serializers.SerializerMethodField()
    more_info_performance_id = serializers.SerializerMethodField()

    type = serializers.CharField(source="common_event.target_model.custom_type", read_only=True, default=None)
    title = serializers.CharField(source="common_event.target_model.name", read_only=True, default=None)
    description = serializers.CharField(source="common_event.target_model.description", read_only=True, default=None)
    team = RoleSerializer(source="common_event.target_model.event_team", many=True)
    image = serializers.ImageField(source="common_event.target_model.main_image", read_only=True, default=None)

    def get_more_info_type(self, obj) -> Optional[str]:
        if isinstance(obj.common_event.target_model, Performance):
            return "performance"

    def get_more_info_performance_id(self, obj) -> Optional[int]:
        if isinstance(obj.common_event.target_model, Performance):
            return obj.common_event.target_model.pk

    class Meta:
        model = Event
        fields = (
            "id",
            "type",
            "title",
            "description",
            "image",
            "more_info_type",
            "more_info_performance_id",
            "team",
        )


class AfishaEventSerializer(BaseEventSerializer):
    """Afisha event Output serializer."""

    action_text = serializers.SerializerMethodField()
    action_url = serializers.SerializerMethodField()

    date_time = serializers.DateTimeField()
    opening_date_time = serializers.DateTimeField()

    def registration_is_open(self, obj):
        """Condition to output registration link and text with the response."""
        return not self.context.get("festival_status") or obj.now > obj.opening_date_time

    def get_action_text(self, obj) -> Optional[str]:
        return obj.get_action_text_display() if self.registration_is_open(obj) else None

    def get_action_url(self, obj) -> Optional[str]:
        return obj.action_url if self.registration_is_open(obj) else None

    class Meta:
        model = Event
        fields = (
            "id",
            "type",
            "title",
            "description",
            "image",
            "date_time",
            "location",
            "action_url",
            "action_text",
            "opening_date_time",
            "more_info_type",
            "more_info_performance_id",
            "team",
        )
