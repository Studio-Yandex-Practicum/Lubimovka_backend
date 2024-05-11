from django.db.models import Q
from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import serializers

from apps.library.models import Author, Play
from apps.library.serializers import AuthorSearchSerializer, PlaySerializer


class SearchResultSerializer(serializers.Serializer):
    """Needed exclusively for the Schema."""

    plays = PlaySerializer(many=True)
    authors = AuthorSearchSerializer(many=True)


@extend_schema(
    parameters=[
        OpenApiParameter(name="q", description="Search parameter", required=False, type=str),
    ],
    responses=SearchResultSerializer,
)
class SearchResultViewSet(ObjectMultipleModelAPIViewSet):
    """
    Поиск авторов по имени и фамилии и пьес по названию.

    При пустом поисковом запросе отдаются пустые массивы.
    """

    pagination_class = None
    queryset = Author.objects.none()  # this needs only for schema generation

    def get_querylist(self):
        """
        Возвращает переменную querylist.

        querylist является списком/кортежем словарей,
        содержащих, как минимум ключи `queryset` и `serializer_class`. Подробнее смотри документацию пакета.
        См. https://django-rest-multiple-models.readthedocs.io/en/latest/filtering.html#override-get-querylist.
        """
        q = self.request.query_params.get("q", "")
        if q:
            plays_queryset = Play.objects.filter(other_play=False, published=True).filter(name__icontains=q)
            authors_queryset = Author.objects.filter(
                Q(person__first_name__unaccent__icontains=q) | Q(person__last_name__unaccent__icontains=q)
            )
        else:
            plays_queryset = Play.objects.none()
            authors_queryset = Author.objects.none()
        querylist = (
            {
                "queryset": plays_queryset,
                "serializer_class": PlaySerializer,
                "label": "plays",
            },
            {
                "queryset": authors_queryset,
                "serializer_class": AuthorSearchSerializer,
                "label": "authors",
            },
        )
        return querylist
