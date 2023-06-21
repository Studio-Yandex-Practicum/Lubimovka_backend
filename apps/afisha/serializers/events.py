from drf_spectacular.utils import PolymorphicProxySerializer, extend_schema_field
from rest_framework import serializers

from apps.afisha.models import Event, Performance, Reading
from apps.afisha.serializers import EventPerformanceSerializer, EventReadingSerializer

AFISHA_EVENTS_SERIALIZER_PAIRS = {
    Performance: EventPerformanceSerializer,
    Reading: EventReadingSerializer,
}


class AfishaEventSerializer(serializers.ModelSerializer):
    """Afisha event Output serializer."""

    action_text = serializers.SerializerMethodField()
    action_url = serializers.SerializerMethodField()

    event_body = serializers.SerializerMethodField(
        help_text="The response is different based on event type.",
    )
    date_time = serializers.DateTimeField()
    opening_date_time = serializers.DateTimeField()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        body = ret.pop("event_body")
        body.pop("id")
        ret.update(body)
        ret.setdefault("custom_type")
        return ret

    def registration_is_open(self, obj):
        """Condition to output registration link and text with the response."""
        return not self.context.get("festival_status") or obj.now > obj.opening_date_time

    def get_action_text(self, obj):
        return obj.get_action_text_display() if self.registration_is_open(obj) else None

    def get_action_url(self, obj):
        return obj.action_url if self.registration_is_open(obj) else None

    @extend_schema_field(
        PolymorphicProxySerializer(
            component_name="Event_Type_objects",
            serializers=AFISHA_EVENTS_SERIALIZER_PAIRS.values(),
            resource_type_field_name=None,
        )
    )
    def get_event_body(self, obj):
        """Get event body type and return serialized data based on it type."""
        event_body = obj.common_event.target_model
        event_model = event_body._meta.model
        serializer_class = AFISHA_EVENTS_SERIALIZER_PAIRS[event_model]
        serializer = serializer_class(event_body, context=self.context)
        return serializer.data

    class Meta:
        model = Event
        fields = ("id", "event_body", "date_time", "location", "action_url", "action_text", "opening_date_time")
