from rest_framework.generics import ListAPIView

from apps.static_pages.models import StaticPagesModel
from apps.static_pages.serializers import StaticPagesSerializer


class IdeologyViewSet(ListAPIView):
    queryset = StaticPagesModel.objects.filter(page_type="ideology")
    serializer_class = StaticPagesSerializer
    pagination_class = None
