from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class YearField(serializers.IntegerField):
    def __init__(self, **kwargs):
        super().__init__(
            label=kwargs.pop("label", _("Год")),
            min_value=kwargs.pop("min_value", 1970),
            max_value=kwargs.pop("max_value", timezone.now().year),
            help_text=kwargs.pop("help_text", _("Максимальный год равен текущему году")),
            **kwargs
        )


class MonthField(serializers.IntegerField):
    def __init__(self, **kwargs):
        super().__init__(
            label=kwargs.pop("label", _("Месяц")),
            min_value=kwargs.pop("min_value", 1),
            max_value=kwargs.pop("max_value", 12),
            **kwargs
        )


class YearListMonthSerializer(serializers.Serializer):
    year = YearField()
    months = serializers.ListSerializer(
        label="Месяцы",
        child=MonthField(),
    )


class YearSerializer(serializers.Serializer):
    """Сериализатор query параметра year."""

    year = YearField(required=False)


class YearMonthSerializer(YearSerializer):
    """Сериализатор query параметров year и month."""

    month = MonthField(required=False)
