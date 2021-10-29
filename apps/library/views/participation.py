from rest_framework import generics

from apps.library.serializers.participation import ParticipationSerializer


class ParticipationAPIView(generics.CreateAPIView):
    serializer_class = ParticipationSerializer
