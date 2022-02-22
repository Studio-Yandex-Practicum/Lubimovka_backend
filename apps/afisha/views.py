from drf_spectacular.utils import PolymorphicProxySerializer, extend_schema, extend_schema_field
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from apps.afisha import selectors
from apps.afisha.models import Event
from apps.afisha.serializers import EventRegularSerializer
from apps.core.fields import CharacterSeparatedSerializerField
from apps.core.utils import get_paginated_response
from apps.library.models import MasterClass, Performance, Reading
from apps.library.serializers import EventMasterClassSerializer, EventPerformanceSerializer, EventReadingSerializer

AFISHA_EVENTS_SERIALIZER_PAIRS = {
    MasterClass: EventMasterClassSerializer,
    Performance: EventPerformanceSerializer,
    Reading: EventReadingSerializer,
}


class AfishaEventsAPIView(APIView):
    """Return events. The response could be filtered by date."""

    class AfishaEventsFilterSerializer(serializers.Serializer):
        """Afisha events filters."""

        dates = CharacterSeparatedSerializerField(
            child=serializers.DateField(required=True),
            required=False,
            help_text=("Support several comma-separared dates. Example: ?dates=2022-04-22,2023-04-25"),
        )

    class AfishaEventsOutputSerializer(serializers.ModelSerializer):
        """Afisha event Output serializer."""

        event_body = serializers.SerializerMethodField(
            help_text="The response is different based on event type.",
        )
        date_time = serializers.DateTimeField()

        @extend_schema_field(
            PolymorphicProxySerializer(
                component_name="Event Type objects",
                serializers=AFISHA_EVENTS_SERIALIZER_PAIRS.values(),
                resource_type_field_name="type",
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
            fields = (
                "id",
                "type",
                "event_body",
                "date_time",
                "paid",
                "url",
                "place",
            )

    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    @extend_schema(
        parameters=[AfishaEventsFilterSerializer],
        responses=AfishaEventsOutputSerializer(many=True),
    )
    def get(self, request):
        filters_serializer = self.AfishaEventsFilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        filtered_events = selectors.afisha_events_get(filters=filters_serializer.data)

        return get_paginated_response(
            pagination_class=self.pagination_class,
            serializer_class=EventRegularSerializer,
            queryset=filtered_events,
            request=request,
            view=self,
        )


class AfishaFestivalStatusAPIView(APIView):
    """Return afisha (affiche) headers and festival status."""

    class AfishaFestivalStatusOutputSerializer(serializers.Serializer):
        festival_status = serializers.BooleanField()
        description = serializers.CharField(max_length=500)
        info_registration = serializers.CharField(max_length=500)
        asterisk_text = serializers.CharField(max_length=500)

    @extend_schema(responses=AfishaFestivalStatusOutputSerializer)
    def get(self, request):
        response_data = selectors.afisha_festival_status()
        context = {"request": request}
        serializer = self.AfishaFestivalStatusOutputSerializer(response_data, context=context)
        return Response(serializer.data)
