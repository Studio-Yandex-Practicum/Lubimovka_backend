from itertools import chain

from django.db.models import QuerySet

from apps.info.filters import PartnerFilterSet
from apps.info.models import Partner


def partner_list(filters: dict[str, str] = None) -> QuerySet:
    """Return filtered queryset of `Partner`."""
    filters = filters or {}
    qs = Partner.objects.all()
    filtered_qs = PartnerFilterSet(data=filters, queryset=qs).qs
    general_qs = filtered_qs.filter(type=Partner.PartnerType.GENERAL_PARTNER)
    festival_qs = filtered_qs.filter(type=Partner.PartnerType.FESTIVAL_PARTNER)
    info_qs = filtered_qs.filter(type=Partner.PartnerType.INFO_PARTNER)
    result = chain(general_qs, festival_qs, info_qs)
    return result
