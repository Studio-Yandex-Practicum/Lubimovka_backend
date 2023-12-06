from rest_framework.generics import ListAPIView

from apps.articles.serializers import YearSerializer
from apps.core.models import Setting
from apps.info.filters import YearFestivalFilterSet
from apps.info.models import Volunteer
from apps.info.serializers import VolunteersSerializer


class VolunteersAPIView(ListAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteersSerializer
    filterset_class = YearFestivalFilterSet
    pagination_class = None

    def get(self, request, *args, **kwargs):
        YearSerializer(data=request.query_params).is_valid(raise_exception=True)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        show = Setting.get_setting("show_volunteers")
        qs = super().get_queryset()
        if not show:
            qs = qs.none()
        return qs
