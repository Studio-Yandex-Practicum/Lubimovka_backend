from rest_framework import generics

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


class ParticipationAPIView(generics.CreateAPIView):
    serializer_class = ParticipationSerializer
