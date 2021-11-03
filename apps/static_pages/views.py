from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveAPIView

from apps.static_pages.models import StaticPagesModel
from apps.static_pages.serializers import StaticPagesSerializer


@extend_schema(
    description="""
        Endpoint for static pages.
        The url parameter takes the appropriate values:

        * what-we-do
        * ideology
        * history

    """
)
class StaticPagesView(RetrieveAPIView):
    queryset = StaticPagesModel.objects.all()
    serializer_class = StaticPagesSerializer

    def get_object(self):
        slug = self.kwargs["static_page_url"]
        obj = get_object_or_404(StaticPagesModel, static_page_url=slug)
        return obj
