from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from apps.core.constants import PlayType
from apps.library.filters import AuthorFilter
from apps.library.models import Author, Play
from apps.library.serializers import AuthorListSerializer, AuthorRetrieveSerializer


class AuthorsReadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.select_related("person").all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AuthorFilter
    lookup_field = "slug"

    def get_object(self):
        author = get_object_or_404(
            Author.objects.prefetch_related(
                "achievements",
                "social_networks",
                "other_links",
                Prefetch("plays", queryset=Play.objects.filter(play_type=PlayType.MAIN)),
            ),
            slug=self.kwargs["slug"],
        )
        return author

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AuthorRetrieveSerializer
        return AuthorListSerializer
