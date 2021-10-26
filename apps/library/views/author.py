from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets

from apps.library.models import Author
from apps.library.serializers import (
    AuthorBasicSerializer,
    AuthorFullSerializer,
)


class AuthorsReadViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ["person__last_name", "person__first_name"]

    def get_queryset(self):
        queryset = Author.objects.order_by("person__last_name")
        first_letter = self.request.query_params.get("startswith")
        if first_letter:
            queryset = queryset.filter(
                person__last_name__startswith=first_letter
            )
        return queryset

    def get_object(self):
        author = get_object_or_404(
            Author.objects.prefetch_related(
                "achievements",
                "social_networks",
                "other_links",
                "plays",
                "other_plays_links",
            ),
            id=self.kwargs["pk"],
        )
        return author

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AuthorFullSerializer
        return AuthorBasicSerializer
