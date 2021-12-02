from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from apps.info.models import PressRelease
from apps.info.serializers import PressReleaseSerializer


class PressReleaseAPIView(ListAPIView):
    queryset = PressRelease.objects.all()
    serializer_class = PressReleaseSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("year",)
