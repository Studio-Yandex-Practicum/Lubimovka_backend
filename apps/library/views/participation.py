from rest_framework import mixins, viewsets

from apps.library.serializers.participation import ParticipationSerializer


class ParticipationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ParticipationSerializer
