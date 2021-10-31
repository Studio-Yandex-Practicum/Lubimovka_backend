from django.contrib import admin

from apps.content_pages.models import Image, Link, Video

admin.site.register(Image)
admin.site.register(Video)
admin.site.register(Link)
