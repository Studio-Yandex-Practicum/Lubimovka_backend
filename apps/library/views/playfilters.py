from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from apps.info.models import Festival
from apps.library.models import ProgramType


class PlayFiltersAPIView(APIView):
    def get(self, request):
        years = list(Festival.objects.values_list("year"))
        programs = list(ProgramType.objects.values_list("name"))
        return JsonResponse(
            {"years": years, "programs": programs},
            status=status.HTTP_200_OK,
            json_dumps_params={"ensure_ascii": False},
        )
