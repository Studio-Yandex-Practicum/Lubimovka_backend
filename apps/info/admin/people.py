from typing import Any

from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.http.request import HttpRequest
from django.urls import reverse
from django.utils.html import format_html

from apps.core.mixins import AdminImagePreview, HideOnNavPanelAdminModelMixin
from apps.core.models import Person
from apps.core.services.mail_forwarding import create_forwarding, delete_forwarding
from apps.info.filters import HasReviewAdminFilter, PartnerTypeFilter
from apps.info.models import Partner, Selector, Sponsor, Volunteer
from apps.info.models.people import Review


@admin.register(Partner)
class PartnerAdmin(SortableAdminMixin, AdminImagePreview, admin.ModelAdmin):
    """Class for registration Partner model in admin panel and expanded with JS script.

    There are used two classes in fieldsets: `predefined` and `included`.
    These classes are not in the documentation and this names are invented
    by developer for the script to work.

    `predefined` - if partners are festival or info.
    `included` - if partner is general.
    """

    list_display = (
        "order",
        "name",
        "description",
        "type",
        "get_partner_url",
        "image_preview_list_page",
    )
    list_display_links = ("name",)
    list_filter = (PartnerTypeFilter,)
    search_fields = ("name",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "description",
                    "type",
                ),
            },
        ),
        (
            None,
            {
                "fields": (
                    "in_footer_partner",
                    "is_general",
                ),
                "classes": ("depended_on_partner_type",),
            },
        ),
        (
            None,
            {
                "fields": (
                    "url",
                    "image",
                    "image_preview_change_page",
                ),
            },
        ),
    )
    empty_value_display = "-пусто-"
    readonly_fields = ("image_preview_change_page",)

    @admin.display(description="Ссылка на сайт")
    def get_partner_url(self, obj):
        """Make the link to the partner's website clickable."""
        return format_html("<a href='{url}'>{url}</a>", url=obj.url)

    class Media:
        """Adds a script that displays the field ```in_footer_partner``` if the general partner is selected."""

        js = ("admin/info/js/PartnerInFooter.js",)


@admin.register(Person)
class PersonAdmin(AdminImagePreview, admin.ModelAdmin):
    list_display = (
        "full_name",
        "first_name",
        "last_name",
        "city",
        "image",
        "image_preview_list_page",
    )
    search_fields = (
        "first_name",
        "last_name",
    )
    empty_value_display = "-пусто-"
    readonly_fields = ("image_preview_change_page",)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if (
            "autocomplete" in request.path
            and request.GET.get("field_name") == "person"
            and request.GET.get("model_name") == "author"
        ):
            person_authors = Person.objects.filter(authors__isnull=False)
            queryset = queryset.difference(person_authors).order_by("last_name", "first_name")
        return queryset, use_distinct

    def get_readonly_fields(self, request: HttpRequest, person: Person) -> tuple[str]:
        return tuple(super().get_readonly_fields(request, person)) + (
            ("email",)
            if not request.user.has_perms(("postfix.change_virtual", "postfix.delete_virtual", "postfix.add_virtual"))
            and person
            and person.has_mail_forwarding
            else ()
        )

    def save_related(self, request: Any, form: Any, formsets: Any, change: Any) -> None:
        person: Person = form.instance
        if "email" in form.changed_data and person.has_mail_forwarding:
            author = person.authors
            if person.email:
                virtual_email = create_forwarding(author)
                messages.add_message(request, messages.INFO, f"Создан виртуальный адрес '{virtual_email}'")
            else:
                virtual_email = delete_forwarding(author)
                messages.add_message(request, messages.INFO, f"Виртуальный адрес '{virtual_email}' был удален")
        super().save_related(request, form, formsets, change)


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = (
        "person",
        "get_year",
        "is_review",
    )
    autocomplete_fields = ("person",)
    readonly_fields = ("is_review",)
    list_filter = (
        "festival",
        HasReviewAdminFilter,
    )

    @admin.display(
        ordering="festival",
        description="Год фестиваля",
    )
    def get_year(self, obj):
        """Возвращает год фестиваля."""
        return obj.festival.year

    @admin.display(
        boolean=True,
        ordering="review_title",
        description="Есть отзыв?",
    )
    def is_review(self, obj):
        """Возвращает: есть ли отзыв."""
        if obj.review_text:
            return True
        return False


@admin.register(Sponsor)
class SponsorAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = (
        "order",
        "person",
        "position",
    )
    list_display_links = ("person",)
    search_fields = ("person__first_name", "person__last_name")
    autocomplete_fields = ("person",)


@admin.register(Selector)
class SelectorAdmin(admin.ModelAdmin):
    list_display = (
        "person",
        "get_year",
        "position",
    )
    autocomplete_fields = ("person",)
    list_filter = ("festival",)

    @admin.display(
        ordering="festival",
        description="Год фестиваля",
    )
    def get_year(self, obj):
        """Возвращает год фестиваля."""
        return obj.festival.year


@admin.register(Review)
class ReviewAdmin(HideOnNavPanelAdminModelMixin, admin.ModelAdmin):
    fields = (
        "review_title",
        "review_text",
    )

    def response_change(self, request, obj):
        super().response_change(request, obj)
        opts = self.model._meta
        redirect_url = reverse(
            "admin:%s_%s_change" % (opts.app_label, "festival"),
            args=(obj.festival_id,),
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(redirect_url)
