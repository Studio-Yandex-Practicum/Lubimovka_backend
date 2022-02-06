from rest_framework.pagination import LimitOffsetPagination


class AfishaPagination(LimitOffsetPagination):
    default_limit = 3
    limit_query_param = "limit"
    offset_query_param = "offset"
    max_limit = None
