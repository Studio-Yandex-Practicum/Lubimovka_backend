from rest_framework.generics import ListAPIView

from apps.core.models import Setting
from apps.info.models import FestivalTeamMember
from apps.info.serializers import FestivalTeamsSerializer


class FestivalTeamsAPIView(ListAPIView):
    queryset = FestivalTeamMember.objects.all()
    serializer_class = FestivalTeamsSerializer
    filterset_fields = ("team",)
    pagination_class = None

    def get_queryset(self):
        show = Setting.get_setting("show_team")
        qs = super().get_queryset()
        if not show:
            qs = qs.none()
        return qs
