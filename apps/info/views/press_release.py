from django.conf import settings
from django.contrib.postgres.aggregates.general import ArrayAgg
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from apps.info.filters import YearPressReleaseFilterSet
from apps.info.models import Festival, PressRelease
from apps.info.serializers.press_release import PressReleaseSerializer
from apps.info.utils import get_pdf_response


class PressReleaseViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = PressReleaseSerializer
    pagination_class = None
    filterset_class = YearPressReleaseFilterSet

    def get_queryset(self):
        if self.request.query_params.get("year"):
            return PressRelease.objects.all()
        return PressRelease.objects.filter(festival=Festival.objects.last())

    @action(
        detail=False,
        methods=("get",),
        url_path="years",
        url_name="years",
        pagination_class=None,
    )
    def years(self, request, **kwargs):
        years = Festival.objects.aggregate(years=ArrayAgg("year"))
        return JsonResponse(
            years,
            status=status.HTTP_200_OK,
            json_dumps_params={"ensure_ascii": False},
        )

    @action(
        detail=False,
        methods=("get",),
        url_path=r"(?P<id>[\d]+)/download",
        url_name="download_press_release",
        pagination_class=None,
    )
    def download_press_release(self, request, id):
        press_release = get_object_or_404(
            PressRelease.objects.select_related("festival"),
            id=id,
        )
        path_to_font = f"{settings.STATIC_ROOT}/fonts/NeueMachinaRegular/PPNeueMachina-Regular.ttf"
        return get_pdf_response(press_release, path_to_font)
