from django.contrib import admin

from apps.info.models import (
    Festival,
    FestivalTeam,
    FestivalVolunteer,
    Partner,
    Person,
    Question,
    Trustee,
    VolunteerReview,
)


class PartnerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "type",
        "url",
        "image",
    )
    empty_value_display = "-пусто-"


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "city",
        "image",
    )
    empty_value_display = "-пусто-"


class FestivalTeamAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "person",
        "team",
    )
    empty_value_display = "-пусто-"


class TrusteeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "person",
    )
    empty_value_display = "-пусто-"


class FestivalVolunteerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "person",
        "year",
    )
    empty_value_display = "-пусто-"


class VolunteerReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "volunteer",
        "review",
    )
    empty_value_display = "-пусто-"


class FestivalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "year",
    )
    empty_value_display = "-пусто-"


class QuestionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Partner, PartnerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(FestivalTeam, FestivalTeamAdmin)
admin.site.register(FestivalVolunteer, FestivalVolunteerAdmin)
admin.site.register(Trustee, TrusteeAdmin)
admin.site.register(VolunteerReview, VolunteerReviewAdmin)
admin.site.register(Festival, FestivalAdmin)
