from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets

from apps.afisha.models import Event
from apps.afisha.pagination import AfishaPagination
from apps.afisha.schema.schema_extension import AFISHA_EVENTS_SCHEMA_DESCRIPTION
from apps.afisha.serializers import EventSerializer


@extend_schema(description=AFISHA_EVENTS_SCHEMA_DESCRIPTION)
class EventsAPIView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Event.objects.filter(date_time__gte=timezone.now()).order_by("date_time")
    serializer_class = EventSerializer
    pagination_class = AfishaPagination
