from django.contrib import admin

from apps.library.models import PerformanceReview
from apps.library.utilities import CustomAutocompleteSelect


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = (
        "reviewer_name",
        "performance",
        "pub_date",
    )
    list_filter = (
        "reviewer_name",
        "performance__name",
        "pub_date",
    )
    autocomplete_fields = ("performance",)
    list_filter = ("pub_date",)
    search_fields = (
        "reviewer_name",
        "performance__name",
        "pub_date",
    )
    readonly_fields = ("pub_date",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "performance":
            db = kwargs.get("using")
            kwargs["widget"] = CustomAutocompleteSelect(
                db_field, self.admin_site, using=db, placeholder="Выберите спектакль"
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
