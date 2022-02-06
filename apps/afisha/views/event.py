from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import views
from rest_framework.pagination import LimitOffsetPagination

from apps.afisha.models import Event
from apps.afisha.schema.schema_extension import AFISHA_EVENTS_SCHEMA_DESCRIPTION
from apps.afisha.serializers import EventSerializerFestival, EventSerializerRegular
from apps.core.models import Setting


class EventsAPIView(LimitOffsetPagination, views.APIView):
    """Add blocks if festival mode is enabled in pagination response.

    info_registration - the text about registration under the description,
    asterisk_text - text with an asterisk near the title.

    And also changes title and description for the festival.
    """

    @extend_schema(
        description=AFISHA_EVENTS_SCHEMA_DESCRIPTION,
        responses=EventSerializerRegular,
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
            dates = set(Event.objects.values_list("date_time__date").filter(date_time__gte=timezone.now()))
            sorted_dates = sorted(list(dates))
            results = []
            for date in sorted_dates:
                query = {"date": date[0], "events": Event.objects.filter(date_time__date=date[0]).order_by("date_time")}
                results.append(query)

            paginated_results = self.paginate_queryset(results, request, view=self)
            serializer = EventSerializerFestival(paginated_results, many=True)
            return self.get_paginated_response(serializer.data)

        queryset = Event.objects.filter(date_time__gte=timezone.now()).order_by("date_time")
        paginated_results = self.paginate_queryset(queryset, request, view=self)
        serializer = EventSerializerRegular(paginated_results, many=True)
        return self.get_paginated_response(serializer.data)

    @property
    def festival_status(self):
        return Setting.get_setting("festival_status")

    # @property
    # def pagination_class(self):
    #     if self.festival_status:
    #         return AfishaPagination
    #     return LimitOffsetPagination

    def finalize_response(self, request, response, *args, **kwargs):
        super(EventsAPIView, self).finalize_response(request, response, *args, **kwargs)

        if self.festival_status:
            response.data["info_registration"] = Setting.get_setting("afisha_info_festival_text")
            response.data["asterisk_text"] = Setting.get_setting("afisha_asterisk_text")
            response.data["title"] = Setting.get_setting("afisha_title_festival")
            response.data["description"] = Setting.get_setting("afisha_description_festival")
        else:
            response.data["title"] = Setting.get_setting("afisha_title_regular")
            response.data["description"] = Setting.get_setting("afisha_description_regular")
        return response
