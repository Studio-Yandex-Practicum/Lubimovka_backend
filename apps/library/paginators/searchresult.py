from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination


class LimitPagination(MultipleModelLimitOffsetPagination):
    default_limit = 100
