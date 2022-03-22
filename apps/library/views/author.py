from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from apps.library.filters import AuthorFilter
from apps.library.models import Author
from apps.library.serializers import AuthorListSerializer, AuthorRetrieveSerializer


class AuthorViewSet(mixins.ListModelMixin, APIView, viewsets.GenericViewSet):
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    queryset = Author.objects.select_related("person")
    serializer = AuthorListSerializer(queryset, many=True)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AuthorFilter


class AuthorRetrieveViewSet(APIView):
    """Returns a list of authors."""

    @extend_schema(responses=AuthorRetrieveSerializer)
    def get(self, request, *args, pk, **kwargs):
        author = get_object_or_404(Author, pk=pk)
        author_serializer = AuthorRetrieveSerializer(author, many=True)
        return Response(author_serializer.data)
