from django.contrib.postgres.aggregates.general import ArrayAgg
from django.http import JsonResponse
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from apps.info.filters import YearPressReleaseFilterSet
from apps.info.models import Festival, PressRelease
from apps.info.serializers.press_release import PressReleaseSerializer


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
