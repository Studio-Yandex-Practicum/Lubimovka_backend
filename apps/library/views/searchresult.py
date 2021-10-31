from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet

from apps.library.models import Author, Play
from apps.library.paginators import LimitPagination
from apps.library.serializers import AuthorForSearchSerializer, PlaySerializer


class SearchResultAPIViewSet(ObjectMultipleModelAPIViewSet):
    pagination_class = LimitPagination

    def get_querylist(self):
        try:
            search = self.request.query_params["search"]
        except MultiValueDictKeyError:
            search = ""
        querylist = (
            {
                "queryset": Play.objects.filter(name__icontains=search),
                "serializer_class": PlaySerializer,
            },
            {
                "queryset": Author.objects.filter(
                    Q(person__first_name__icontains=search)
                    | Q(person__last_name__icontains=search)
                ),
                "serializer_class": AuthorForSearchSerializer,
            },
        )
        return querylist
