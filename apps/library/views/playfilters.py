from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.info.models import Festival
from apps.library.models import ProgramType
from apps.library.serializers.playfilters import PlayFiltersSerializer


class PlayFiltersAPIView(APIView):
    @extend_schema(responses=PlayFiltersSerializer)
    def get(self, request):
        years = Festival.objects.all()
        programs = ProgramType.objects.all()
        filter_instance = {"programs": programs, "years": years}
        serialized_data = PlayFiltersSerializer(instance=filter_instance).data
        return Response(
            serialized_data,
            status=status.HTTP_200_OK,
        )
