from django.shortcuts import get_object_or_404
from django.urls import reverse
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.permissions import IsAdminUser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from apps.afisha import selectors
from apps.afisha.models import CommonEvent, Event
from apps.afisha.serializers import AfishaEventSerializer
from apps.core.fields import CharacterSeparatedSerializerField
from apps.core.utils import get_paginated_response

POPUP_SUFFIX = "?_popup=1"


class AfishaEventListAPIView(APIView):
    """Return events. The response could be filtered by date."""

    class AfishaEventListFilterSerializer(serializers.Serializer):
        """Afisha events filters."""

        dates = CharacterSeparatedSerializerField(
            child=serializers.DateField(required=True),
            required=False,
            help_text="Принимает одну или несколько дат через запятую. Пример: ?dates=2022-04-22,2023-04-25",
        )

    class AfishaEventListOutputSerializer(AfishaEventSerializer):
        pass

    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    @extend_schema(
        parameters=[AfishaEventListFilterSerializer],
        responses=AfishaEventListOutputSerializer(many=True),
    )
    def get(self, request):
        filters_serializer = self.AfishaEventListFilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        filtered_events = selectors.afisha_event_list_get(filters=filters_serializer.data)

        return get_paginated_response(
            pagination_class=self.pagination_class,
            serializer_class=self.AfishaEventListOutputSerializer,
            queryset=filtered_events,
            request=request,
            view=self,
        )


class AfishaInfoAPIView(APIView):
    """Return afisha (affiche) headers and festival status."""

    class AfishaInfoOutputSerializer(serializers.Serializer):
        festival_status = serializers.BooleanField(
            help_text="Статус фестиваля. Идёт или нет.",
        )
        description = serializers.CharField(
            source="afisha_description",
            max_length=500,
            help_text="Текст под заголовком афиши.",
        )
        info_registration = serializers.CharField(
            source="afisha_info_festival_text",
            max_length=500,
            required=False,
            help_text="Текст под заголовком афиши о регистрации. Есть в выдаче только когда `festival_status=true`.",
        )
        asterisk_text = serializers.CharField(
            source="afisha_asterisk_text",
            max_length=500,
            required=False,
            help_text="Текст под знаком `*`. Есть в выдаче только когда `festival_status=true`.",
        )
        afisha_dates = serializers.ListField(
            child=serializers.DateField(),
            help_text="Список дат на которые есть хотя бы одно событие.",
        )

    @extend_schema(responses=AfishaInfoOutputSerializer)
    def get(self, request):
        response_data = selectors.afisha_info_get()
        context = {"request": request}
        serializer = self.AfishaInfoOutputSerializer(response_data, context=context)
        return Response(serializer.data)


class GetCommonEventsAdmin(APIView):
    """Return common events for the event type."""

    permission_classes = [IsAdminUser]
    renderer_classes = [JSONRenderer]

    class AdminCommonEventSerializer(serializers.Serializer):
        type = serializers.CharField(required=False)

    @extend_schema(exclude=True)
    def post(self, request):
        data_type_serializer = self.AdminCommonEventSerializer(data=request.data)
        data_type_serializer.is_valid(raise_exception=True)
        data = data_type_serializer.validated_data
        common_event_type = data.get("type")
        common_events = {}
        if common_event_type:
            common_events_queryset = Event.objects.filter(type=common_event_type)
            common_events = {
                event.common_event.target_model.name: event.common_event.target_model.id
                for event in common_events_queryset
            }
        return Response(common_events)


@extend_schema(exclude=True)
class GetCommonEventLink(APIView):
    """Return URL link to add or change based on `model_id` and `object_id`."""

    permission_classes = [IsAdminUser]

    class QueryParamSerializer(serializers.Serializer):
        common_event_id = serializers.IntegerField()

    def get(self, request):
        query_params_serializer = self.QueryParamSerializer(data=request.query_params)
        query_params_serializer.is_valid(raise_exception=True)
        data = query_params_serializer.validated_data

        common_event_id = data.get("common_event_id")
        response_url_data = {}
        link_types = ["add", "change"]

        common_event = get_object_or_404(CommonEvent, id=common_event_id)
        common_event_model = common_event.target_model

        for link_type in link_types:
            reverse_args = (common_event_id,) if link_type == "change" and common_event_id else None
            url = reverse(
                f"admin:{common_event_model._meta.app_label}_{(common_event_model._meta.object_name).lower()}_{link_type}",  # Noqa
                args=reverse_args,
            )
            url += POPUP_SUFFIX
            response_url_data["url_" + link_type] = url
        return Response(data=response_url_data, status=status.HTTP_200_OK)
