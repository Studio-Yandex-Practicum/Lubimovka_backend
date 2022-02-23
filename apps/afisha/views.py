from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from apps.afisha import selectors
from apps.afisha.serializers import AfishaEventSerializer
from apps.core.fields import CharacterSeparatedSerializerField
from apps.core.utils import get_paginated_response


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
        filtered_events = selectors.afisha_events_get(filters=filters_serializer.data)

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
        festival_status = serializers.BooleanField()
        description = serializers.CharField(max_length=500)
        info_registration = serializers.CharField(max_length=500)
        asterisk_text = serializers.CharField(max_length=500)

    @extend_schema(responses=AfishaInfoOutputSerializer)
    def get(self, request):
        response_data = selectors.afisha_festival_status()
        context = {"request": request}
        serializer = self.AfishaInfoOutputSerializer(response_data, context=context)
        return Response(serializer.data)
