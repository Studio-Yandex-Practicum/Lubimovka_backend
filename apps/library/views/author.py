from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from apps.library.filters import AuthorFilter
from apps.library.models import Author
from apps.library.serializers import AuthorListSerializer, AuthorRetrieveSerializer


class AuthorsReadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.select_related("person").all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AuthorFilter

    def get_object(self):
        author = get_object_or_404(
            Author.objects.prefetch_related(
                "achievements",
                "social_networks",
                "other_links",
                "plays",
                "publications",
                "other_plays",
            ),
            id=self.kwargs["pk"],
        )
        return author

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AuthorRetrieveSerializer
        return AuthorListSerializer
