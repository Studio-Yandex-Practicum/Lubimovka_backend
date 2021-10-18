from rest_framework import mixins, viewsets

from apps.afisha.models import Event
from apps.afisha.serializers.event import EventSerializer


class EventsAPIView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
