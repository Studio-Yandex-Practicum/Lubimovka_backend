from django.contrib import admin

from apps.content_pages.models import Image, Link, Quote, Text, Title, Video

admin.site.register(Image)
admin.site.register(Link)
admin.site.register(Quote)
admin.site.register(Text)
admin.site.register(Title)
admin.site.register(Video)
