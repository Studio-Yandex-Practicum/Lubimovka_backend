from django.contrib import admin

from apps.main.models import Banner


class BannerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
        "url",
    )


admin.site.register(Banner, BannerAdmin)
