from django.utils import timezone
from rest_framework import mixins, viewsets

from apps.afisha.models import Event
from apps.afisha.pagination import AfishaPagination
from apps.afisha.serializers import EventSerializer


class EventsAPIView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Event.objects.filter(date_time__gte=timezone.now()).order_by("date_time")
    serializer_class = EventSerializer
    pagination_class = AfishaPagination
