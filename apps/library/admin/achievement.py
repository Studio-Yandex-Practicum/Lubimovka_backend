from django.contrib import admin

from apps.library.models import Achievement


class AchievementAdmin(admin.ModelAdmin):
    list_display = ("tag",)


admin.site.register(Achievement, AchievementAdmin)
