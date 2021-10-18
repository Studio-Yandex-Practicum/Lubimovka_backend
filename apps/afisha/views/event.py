from rest_framework import mixins, viewsets

from apps.afisha.models import Event
from apps.afisha.serializers import EventSerializer


class EventsAPIView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
