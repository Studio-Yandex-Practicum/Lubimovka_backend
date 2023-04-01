from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import PolymorphicProxySerializer, extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.afisha.models import Performance
from apps.afisha.serializers import PerformanceTypedSerializer
from apps.library.models import Author, AuthorPlay
from apps.library.serializers import AuthorTypedSerializer


class SlugDetermineAPI(APIView):
    """Determine which slug came - performance or author and return object or 404."""

    @extend_schema(
        responses=PolymorphicProxySerializer(
            component_name="typed_performance_or_author",
            serializers=(PerformanceTypedSerializer, AuthorTypedSerializer),
            resource_type_field_name=None,
        )
    )
    def get(self, request, identifier):
        context = {"request": request}
        performances_slug_list = Performance.objects.all().values_list("slug", flat=True)

        if identifier in performances_slug_list:
            performance = Performance.objects.get(slug=identifier)
            serializer = PerformanceTypedSerializer(performance, context=context)

        else:
            author = get_object_or_404(
                Author.objects.prefetch_related(
                    "social_networks",
                    "other_links",
                    Prefetch(
                        "author_plays",
                        queryset=AuthorPlay.objects.filter(
                            play__other_play=False, play__published=True
                        ).prefetch_related("play__authors__person"),
                    ),
                    Prefetch(
                        "author_plays",
                        queryset=AuthorPlay.objects.filter(
                            play__other_play=True, play__published=True
                        ).prefetch_related("play__authors__person"),
                        to_attr="other_plays",
                    ),
                ).select_related("person"),
                slug=identifier,
            )
            serializer = AuthorTypedSerializer(author, context=context)

        return Response(serializer.data)
