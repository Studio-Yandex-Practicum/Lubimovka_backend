from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.library.serializers.participation import ParticipationSerializer


class PlaysAPIView(generics.ListAPIView):
    pass


class PerformancesAPIView(generics.ListAPIView):
    pass


class AuthorsAPIView(generics.ListAPIView):
    pass


class PerformanceMediaReviewsAPIView(generics.ListAPIView):
    pass


class PerformanceReviewsAPIView(generics.ListAPIView):
    pass


class ParticipationCreateAPI(generics.CreateAPIView):
    serializer_class = ParticipationSerializer
    permission_classes = [AllowAny]
