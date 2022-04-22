from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.info import selectors
from apps.info.serializers import SettingsSerializer


class SettingsAPIView(APIView):
    @extend_schema(request=None, responses=SettingsSerializer)
    def get(self, request):
        """Get all required emails that can be changed.

        except email on contacts page
        """
        response_data = selectors.feedback_settings_get()
        context = {"request": request}
        serializer = SettingsSerializer(response_data, context=context)
        return Response(serializer.data)
