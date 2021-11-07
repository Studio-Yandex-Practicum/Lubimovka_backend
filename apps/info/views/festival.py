from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView

from apps.info.models import Festival
from apps.info.serializers import FestivalSerializer


class FestivalViewSet(RetrieveAPIView):
    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer
    lookup_field = "year"
    pagination_class = None


@api_view(["GET"])
def festivals_years(request):
    data = list(
        festival["year"] for festival in Festival.objects.values("year")
    )
    return JsonResponse({"years": data}, status=status.HTTP_200_OK)
