from rest_framework.pagination import LimitOffsetPagination


class EventPaginationMixin(object):
    @property
    def paginator(self):
        """Paginator instance associated with the view, or `None`."""
        if not hasattr(self, "_paginator"):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """Return a single page of results, or `None` if pagination is disabled."""
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """Return a paginated style `Response` object for the given output data."""
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class AfishaFestivalPagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = None


class AfishaRegularPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = None
