from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.content_pages.models import Content
from apps.content_pages.serializers import BaseContentSerializer


class ContentViewSet(ReadOnlyModelViewSet):
    queryset = Content.objects.all()
    serializer_class = BaseContentSerializer
    permission_classes = [AllowAny]

    class Meta:
        model = Content
