from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.main.serializers import MainSerializer
from apps.main.utilities import MainObject


class MainView(APIView):
    @extend_schema(responses=MainSerializer)
    def get(self, request):
        main = MainObject()
        main.add_first_screen_data()
        main.add_blog_data()
        main.add_news_data()
        main.add_afisha()
        main.add_banners()
        main.add_short_list()
        main.add_video_archive()
        main.add_places()
        # Common access to context. It's required to return correct url links
        context = {
            "request": self.request,
            "festival_status": main.settings.get("festival_status"),
        }
        main_serializer = MainSerializer(main, context=context)
        return Response(main_serializer.data)
