from rest_framework import serializers

from apps.afisha.models import Event
from apps.library.models import MasterClass, Performance, Reading
from apps.library.serializers import (
    EventMasterClassSerializer,
    EventPerformanceSerializer,
    EventReadingSerializer,
)


class EventSerializer(serializers.ModelSerializer):
    event_body = serializers.SerializerMethodField()
    date_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M")

    def get_event_body(self, obj):
        event_body_serializers = {
            MasterClass: EventMasterClassSerializer,
            Performance: EventPerformanceSerializer,
            Reading: EventReadingSerializer,
        }
        event_body = obj.common_event.target_model
        event_type = type(event_body)
        serializer = event_body_serializers[event_type]
        return serializer(event_body).data

    class Meta:
        model = Event
        fields = (
            "id",
            "type",
            "event_body",
            "date_time",
            "paid",
            "url",
            "place",
        )
