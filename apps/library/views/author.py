from django.db.models import Prefetch
from django.db.models.functions import Substr
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.library.filters import AuthorFilter
from apps.library.models import Author, AuthorPlay
from apps.library.schema_extension import ERROR_MESSAGES_FOR_AUTHOR_FOR_403
from apps.library.serializers import AuthorLettersSerializer, AuthorListSerializer, AuthorRetrieveSerializer


class AuthorsReadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.select_related("person").all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AuthorFilter
    lookup_field = "slug"

    @extend_schema(
        responses={
            200: AuthorListSerializer,
            403: ERROR_MESSAGES_FOR_AUTHOR_FOR_403,
        }
    )
    def list(self, request):
        if not request.query_params.get("letter"):
            raise PermissionDenied("Укажите параметр - letter.")
        return super().list(self, request)

    def get_object(self):
        author = get_object_or_404(
            Author.objects.prefetch_related(
                "social_networks",
                "other_links",
                Prefetch(
                    "author_plays",
                    queryset=AuthorPlay.objects.filter(play__other_play=False, play__published=True).prefetch_related(
                        "play__authors__person"
                    ),
                ),
                Prefetch(
                    "author_plays",
                    queryset=AuthorPlay.objects.filter(play__other_play=True, play__published=True).prefetch_related(
                        "play__authors__person"
                    ),
                    to_attr="other_plays",
                ),
            ).select_related("person"),
            slug=self.kwargs["slug"],
        )
        return author

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AuthorRetrieveSerializer
        return AuthorListSerializer


class AuthorLettersAPIView(APIView):
    """Returns a list of the first letters of the available authors' surnames."""

    @extend_schema(responses=AuthorLettersSerializer)
    def get(self, request):
        authors_list = Author.objects.annotate(letter=Substr("person__last_name", pos=1, length=1)).values("letter")
        letters_values_list = list({author.get("letter") for author in authors_list})
        letters_instance = {"letters": letters_values_list}
        serializer = AuthorLettersSerializer(instance=letters_instance)
        return Response(serializer.data)
