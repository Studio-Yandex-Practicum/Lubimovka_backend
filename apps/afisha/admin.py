from django.contrib import admin

from apps.afisha.models import Afisha


class AfishaAdmin(admin.ModelAdmin):
    pass


admin.site.register(Afisha, AfishaAdmin)
