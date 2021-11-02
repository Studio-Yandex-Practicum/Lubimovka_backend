from django.db.models import Q
from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet

from apps.library.models import Author, Play
from apps.library.paginators import LimitPagination
from apps.library.serializers import AuthorForSearchSerializer, PlaySerializer


class SearchResultAPIViewSet(ObjectMultipleModelAPIViewSet):
    pagination_class = LimitPagination

    def get_querylist(self):
        q = self.request.query_params.get("q", "")
        querylist = (
            {
                "queryset": Play.objects.filter(name__icontains=q),
                "serializer_class": PlaySerializer,
            },
            {
                "queryset": Author.objects.filter(
                    Q(person__first_name__icontains=q)
                    | Q(person__last_name__icontains=q)
                ),
                "serializer_class": AuthorForSearchSerializer,
            },
        )
        return querylist
