from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.library.filters import AuthorFilter
from apps.library.models import Author
from apps.library.schema.schema_extension import ERROR_MESSAGES_FOR_AUTHOR_FOR_403
from apps.library.serializers import AuthorLettersSerializer, AuthorListSerializer, AuthorRetrieveSerializer


@extend_schema(
    responses={
        201: AuthorListSerializer,
        403: ERROR_MESSAGES_FOR_AUTHOR_FOR_403,
    }
)
class AuthorsReadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.select_related("person").all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AuthorFilter
    lookup_field = "slug"

    def list(self, request):
        if self.action == "list" and not request.query_params.get("letter"):
            raise PermissionDenied("Укажите параметр - letter.")
        return super().list(self, request)

    def get_object(self):
        author = get_object_or_404(
            Author.objects.prefetch_related(
                "achievements",
                "social_networks",
                "other_links",
                "plays",
                "other_plays",
            ),
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
        authors_list = Author.objects.select_related("person").all()
        letters_values_list = [author.person.last_name[0] for author in authors_list]
        letters_values_list_without_double = sorted(list(set(letters_values_list)))
        letters_instance = {"letters": letters_values_list_without_double}
        serializer = AuthorLettersSerializer(instance=letters_instance)
        return Response(serializer.data)
