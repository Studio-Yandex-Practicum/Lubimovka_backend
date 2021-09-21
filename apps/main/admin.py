from django.contrib import admin

from apps.main.models import MainPage


class MainPageAdmin(admin.ModelAdmin):
    pass


admin.site.register(MainPage, MainPageAdmin)
