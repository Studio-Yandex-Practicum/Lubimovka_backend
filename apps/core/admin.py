from django.contrib import admin

from apps.core.models import Image


class ImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)
