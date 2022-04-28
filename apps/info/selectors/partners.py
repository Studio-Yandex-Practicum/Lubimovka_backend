from django.db.models import QuerySet

from apps.info.filters import PartnerFilterSet
from apps.info.models import Partner


def partner_list(filters: dict[str, str] = None) -> QuerySet:
    """Return filtered queryset of `Partner`."""
    filters = filters or {}
    qs = Partner.objects.all()
    filtered_qs = PartnerFilterSet(data=filters, queryset=qs).qs
    return filtered_qs
