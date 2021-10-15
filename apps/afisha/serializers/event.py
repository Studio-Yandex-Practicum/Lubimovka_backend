from rest_framework import serializers

from apps.afisha.models import Event
from apps.library.models import MasterClass, Performance, Reading
from apps.library.serializers.masterclass import MasterClassEventSerializer
from apps.library.serializers.performance import PerformanceEventSerializer
from apps.library.serializers.reading import ReadingEventSerializer


class EventSerializer(serializers.ModelSerializer):
    event_body = serializers.SerializerMethodField()
    date_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M")

    def get_event_body(self, obj):
        event_body_serializers = {
            MasterClass: MasterClassEventSerializer,
            Performance: PerformanceEventSerializer,
            Reading: ReadingEventSerializer,
        }
        event_body = obj.common_event.target_model
        return event_body_serializers[type(event_body)](event_body).data

    class Meta:
        model = Event
        fields = [
            "id",
            "type",
            "event_body",
            "date_time",
            "paid",
            "url",
            "place",
        ]
