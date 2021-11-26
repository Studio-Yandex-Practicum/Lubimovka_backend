from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from apps.info.models import Festival
from apps.library.models import ProgramType


@api_view(["GET"])
def filters(request):
    years = list(
        festival["year"] for festival in Festival.objects.values("year")
    )
    programs = list(
        program["name"] for program in ProgramType.objects.values("name")
    )
    return JsonResponse(
        {"years": years, "programs": programs},
        status=status.HTTP_200_OK,
        json_dumps_params={"ensure_ascii": False},
    )
