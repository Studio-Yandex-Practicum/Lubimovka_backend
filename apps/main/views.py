from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.main.models import MainSettings
from apps.main.serializers import MainSettigsSerializer


class MainApiView(generics.ListAPIView):
    serializer_class = MainSettigsSerializer
    permission_classes = [AllowAny]
    queryset = MainSettings.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["type", "settings_key"]
