from django.contrib import admin

from apps.content_pages.models import Link, Preamble, Quote, Text, Title, Video
from apps.core.mixins import HideOnNavPanelAdminModelMixin


class ModelAdminToHide(HideOnNavPanelAdminModelMixin, admin.ModelAdmin):
    pass


admin.site.register(Preamble, ModelAdminToHide)
admin.site.register(Link, ModelAdminToHide)
admin.site.register(Quote, ModelAdminToHide)
admin.site.register(Text, ModelAdminToHide)
admin.site.register(Title, ModelAdminToHide)
admin.site.register(Video, ModelAdminToHide)
