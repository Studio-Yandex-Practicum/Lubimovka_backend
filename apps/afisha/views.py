from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.afisha import selectors
from apps.afisha.models import Event
from apps.afisha.pagination import AfishaFestivalPagination, AfishaRegularPagination, EventPaginationMixin
from apps.afisha.schema.schema_extension import AFISHA_EVENTS_SCHEMA_DESCRIPTION
from apps.afisha.serializers import EventFestivalSerializer, EventRegularSerializer
from apps.core.models import Setting


class EventsAPIView(EventPaginationMixin, APIView):
    """Returns the response depending festival mode on the settings.

    Add in finalize_response on the settings:
        festival_status - True or False
        description -  text under title in the afisha page

        blocks if festival mode is enabled in pagination response:
        info_registration - the text about registration under the description,
        asterisk_text - text with an asterisk near the title.

    """

    @extend_schema(
        description=AFISHA_EVENTS_SCHEMA_DESCRIPTION,
        responses=EventRegularSerializer,
        parameters=[
            OpenApiParameter(
                "limit",
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                description="Number of results to return per page.",
            ),
            OpenApiParameter(
                "offset",
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                description="The initial index from which to return the results.",
            ),
        ],
    )
    def get(self, request):
        if self.festival_status:
            dates_queryset = (
                Event.objects.filter(date_time__gte=timezone.now()).order_by("date").distinct("date").values("date")
            )
            results = []
            if dates_queryset:
                for date in dates_queryset:
                    events_in_date = {
                        "date": date["date"],
                        "events": Event.objects.filter(date_time__date=date["date"]).order_by("date_time"),
                    }
                    results.append(events_in_date)

            paginated_results = self.paginate_queryset(results)
            serializer = EventFestivalSerializer(paginated_results, many=True)
            return self.get_paginated_response(serializer.data)

        queryset = Event.objects.filter(date_time__gte=timezone.now()).order_by("date_time")
        paginated_results = self.paginate_queryset(queryset)
        serializer = EventRegularSerializer(paginated_results, many=True)
        return self.get_paginated_response(serializer.data)

    @property
    def festival_status(self):
        return Setting.get_setting("festival_status")

    @property
    def pagination_class(self):
        if self.festival_status:
            return AfishaFestivalPagination
        return AfishaRegularPagination

    def finalize_response(self, request, response, *args, **kwargs):
        super(EventsAPIView, self).finalize_response(request, response, *args, **kwargs)
        response.data["festival_status"] = self.festival_status
        response.data["description"] = Setting.get_setting("afisha_description")

        if self.festival_status:
            response.data["info_registration"] = Setting.get_setting("afisha_info_festival_text")
            response.data["asterisk_text"] = Setting.get_setting("afisha_asterisk_text")
        return response


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
