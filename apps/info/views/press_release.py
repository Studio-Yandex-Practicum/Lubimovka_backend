from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.models import Setting
from apps.info.models import PressRelease
from apps.info.serializers.festival import YearsSerializer
from apps.info.serializers.press_release import PhotoGalleryLinkSerializer, PressReleaseSerializer
from apps.info.utils import get_pdf_response


class PressReleaseViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = PressRelease.objects.all()
    serializer_class = PressReleaseSerializer
    lookup_field = "festival__year"
    pagination_class = None


class PressReleaseYearsAPIView(APIView):
    def get(self, request):
        """Get a list of years for which there are press releases."""
        years_values_list = PressRelease.objects.values_list("festival__year", flat=True)
        years_instance = {"years": years_values_list}
        years_serializer = YearsSerializer(instance=years_instance)
        return Response(years_serializer.data)


class PressReleaseDownloadAPIView(APIView):
    def get(self, request, festival__year):
        """Get a press-release pdf file."""
        press_release = get_object_or_404(PressRelease, festival__year=festival__year)
        path_to_font = f"{settings.STATIC_ROOT}/fonts/NeueMachinaRegular/PPNeueMachina-Regular.ttf"
        return get_pdf_response(press_release, path_to_font)


class PressReleasePhotoGalleryLink(APIView):
    def get(self, request):
        link = Setting.get_setting("photo_gallery_facebook")
        photo_gallery_facebook_link = {"photo_gallery_facebook_link": link}
        url_serializer = PhotoGalleryLinkSerializer(photo_gallery_facebook_link)
        return Response(url_serializer.data)
