from rest_framework import generics, permissions

from .models import Place
from .serializers import PlaceSerializer


class PartnersAPIView(generics.ListAPIView):
    pass


class QuestionsAPIView(generics.ListAPIView):
    pass


class PlaceAPIView(generics.ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [permissions.AllowAny]
