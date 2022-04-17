from django.contrib import admin

from apps.content_pages.models import ContentUnitRichText, Link, Preamble, Quote, Text, Title
from apps.core.mixins import HideOnNavPanelAdminModelMixin


class ModelAdminToHide(HideOnNavPanelAdminModelMixin, admin.ModelAdmin):
    pass


admin.site.register(ContentUnitRichText, ModelAdminToHide)
admin.site.register(Preamble, ModelAdminToHide)
admin.site.register(Link, ModelAdminToHide)
admin.site.register(Quote, ModelAdminToHide)
admin.site.register(Text, ModelAdminToHide)
admin.site.register(Title, ModelAdminToHide)
