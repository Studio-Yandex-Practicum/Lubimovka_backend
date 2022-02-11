from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from apps.afisha.models import Event
from apps.afisha.schema.schema_extension import (
    SUCCESS_MESSAGE_FOR_AFISHA_EVENTS_FOR_200_FESTIVAL,
    SUCCESS_MESSAGE_FOR_AFISHA_EVENTS_FOR_200_REGULAR,
)
from apps.library.models import MasterClass, Performance, Reading
from apps.library.serializers import EventMasterClassSerializer, EventPerformanceSerializer, EventReadingSerializer


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            name="Schema for afisha with festival setup",
            summary="Festival setup",
            value=SUCCESS_MESSAGE_FOR_AFISHA_EVENTS_FOR_200_FESTIVAL,
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            name="Schema for afisha with regular setup",
            summary="Regular setup",
            value=SUCCESS_MESSAGE_FOR_AFISHA_EVENTS_FOR_200_REGULAR,
            request_only=False,
            response_only=True,
        ),
    ],
)
class EventRegularSerializer(serializers.ModelSerializer):
    """Returns events on afisha page if festival_status == False on the settings."""

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


class EventFestivalSerializer(serializers.Serializer):
    """Returns events for date on afisha page if festival_status == True on the settings."""

    date = serializers.DateField()
    events = EventRegularSerializer(many=True)
