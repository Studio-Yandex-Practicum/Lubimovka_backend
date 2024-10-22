from django.contrib import admin

from apps.content_pages.models import ContentUnitRichText, EmbedCode, Link
from apps.core.mixins import HideOnNavPanelAdminModelMixin


class ModelAdminToHide(HideOnNavPanelAdminModelMixin, admin.ModelAdmin):
    pass


admin.site.register(ContentUnitRichText, ModelAdminToHide)
admin.site.register(Link, ModelAdminToHide)
admin.site.register(EmbedCode, ModelAdminToHide)
