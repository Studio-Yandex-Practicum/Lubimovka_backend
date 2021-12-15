from django.contrib.postgres.aggregates.general import ArrayAgg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from xhtml2pdf import pisa

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

    @action(
        detail=False,
        methods=("get",),
        url_path=r"(?P<id>[\d]+)/download",
        url_name="download_press_release",
        pagination_class=None,
    )
    def download_press_release(self, request, **kwargs):
        press_release = get_object_or_404(
            PressRelease.objects.select_related("festival"),
            id=kwargs["id"],
        )
        press_release_year = press_release.festival.year
        response = HttpResponse(content_type="application/pdf")
        response[
            "Content-Disposition"
        ] = f"attachment; filename='press-release_{press_release_year}.pdf'"
        template = get_template("press_release.html")
        content = template.render({"press_release": press_release})
        pisa_status = pisa.CreatePDF(
            content,
            dest=response,
            encoding="UTF-8",
        )
        if pisa_status.err:
            return HttpResponse(
                "Пожалуйста, попробуйте повторить попытку позже"
            )
        return response
