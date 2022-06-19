from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from apps.info.models import Place


@admin.register(Place)
class PlaceAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = (
        "order",
        "name",
        "city",
        "address",
    )
    list_display_links = ("name",)
    list_filter = ("city",)
    search_fields = ("name", "address")
