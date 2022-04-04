from django.conf import settings
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiTypes, extend_schema
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.info.models import PressRelease
from apps.info.serializers.festival import YearsSerializer
from apps.info.serializers.press_release import PressReleaseSerializer
from apps.info.utils import get_pdf_response


class PressReleaseViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = PressRelease.objects.all()
    serializer_class = PressReleaseSerializer
    lookup_field = "festival__year"
    pagination_class = None


@extend_schema(responses={200: YearsSerializer})
class PressReleaseYearsAPIView(APIView):
    def get(self, request):
        """Get a list of years for which there are press releases."""
        years_values_list = PressRelease.objects.values_list("festival__year", flat=True)
        years_instance = {"years": years_values_list}
        years_serializer = YearsSerializer(instance=years_instance)
        return Response(years_serializer.data)


@extend_schema(
    responses={
        (200, "application/pdf"): OpenApiTypes.NONE,
    }
)
class PressReleaseDownloadAPIView(APIView):
    def get(self, request, festival__year):
        """Get a press-release pdf file."""
        press_release = get_object_or_404(PressRelease, festival__year=festival__year)
        path_to_font = f"{settings.STATIC_ROOT}/fonts/NeueMachinaRegular/PPNeueMachina-Regular.ttf"
        return get_pdf_response(press_release, path_to_font)
