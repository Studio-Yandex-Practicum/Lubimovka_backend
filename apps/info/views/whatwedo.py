from rest_framework.generics import ListAPIView

from apps.static_pages.models import StaticPagesModel
from apps.static_pages.serializers import StaticPagesSerializer


class WhatWeDoViewSet(ListAPIView):
    queryset = StaticPagesModel.objects.filter(page_type="what-we-do")
    serializer_class = StaticPagesSerializer
    pagination_class = None
