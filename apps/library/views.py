from rest_framework import generics


class PlaysAPIView(generics.ListAPIView):
    pass


class SpectaclesAPIView(generics.ListAPIView):
    pass


class AuthorsAPIView(generics.ListAPIView):
    pass


class MediaReviewsSpectacleAPIView(generics.ListAPIView):
    pass


class WatcherReviewsSpectacleAPIView(generics.ListAPIView):
    pass
