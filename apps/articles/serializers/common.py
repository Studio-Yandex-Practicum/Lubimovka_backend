from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class YearField(serializers.IntegerField):
    def __init__(self, **kwargs):
        kwargs["label"] = _("Год")
        kwargs["min_value"] = 1970
        kwargs["max_value"] = timezone.now().year
        kwargs["help_text"] = _("Максимальный год равен текущему году")
        super().__init__(**kwargs)


class MonthField(serializers.IntegerField):
    def __init__(self, **kwargs):
        kwargs["label"] = _("Месяц")
        kwargs["min_value"] = 1
        kwargs["max_value"] = 12
        super().__init__(**kwargs)


class YearMonthSerializer(serializers.Serializer):
    year = YearField()
    months = serializers.ListSerializer(
        child=MonthField(),
        label="Месяцы",
    )


class QueryYearParamSerializer(serializers.Serializer):
    """Сериализатор query параметра year."""

    year = YearField(required=False)


class QueryYearMonthParamsSerializer(QueryYearParamSerializer):
    """Сериализатор query параметров year и month."""

    month = MonthField(required=False)
