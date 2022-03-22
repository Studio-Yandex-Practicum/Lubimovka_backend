from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from apps.core.mixins import AdminImagePreview
from apps.core.models import Person, Setting
from apps.info.form import ArtTeamMemberForm
from apps.info.models import Festival, FestivalTeamMember, Partner, Place, PressRelease, Question, Sponsor, Volunteer
from apps.info.models.festival import ArtTeamMember, FestTeamMember


@admin.register(Partner)
class PartnerAdmin(AdminImagePreview, admin.ModelAdmin):
    """Class for registration Partner model in admin panel and expanded with JS script.

    There are used two classes in fieldsets: `predefined` and `included`.
    These classes are not in the documentation and this names are invented
    by developer for the script to work.

    `predefined` - if partners are festival or info.
    `included` - if partner is general.
    """

    list_display = (
        "name",
        "type",
        "get_partner_url",
        "image_preview_list_page",
    )
    list_filter = ("type",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "type",
                ),
            },
        ),
        (
            None,
            {
                "fields": ("in_footer_partner",),
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
    empty_value_display = "-пусто-"
    readonly_fields = ("image_preview_change_page",)


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = (
        "person",
        "get_year",
        "is_review",
    )
    readonly_fields = ("is_review",)

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

    @admin.display(
        ordering="festival",
        description="Год фестиваля",
    )
    def get_year(self, obj):
        """Возвращает год фестиваля."""
        return obj.festival.year


class VolunteerInline(admin.TabularInline):
    model = Volunteer
    readonly_fields = ("is_review",)
    verbose_name = "Волонтёр"
    verbose_name_plural = "Волонтёры"
    extra = 1
    exclude = (
        "review_title",
        "review_text",
    )
    classes = ["collapse"]
    ordering = ("person__last_name", "person__first_name")

    @admin.display(
        boolean=True,
        ordering="review_title",
        description="Есть отзыв?",
    )
    def is_review(self, obj):
        if obj.review_text:
            return True
        return False


class FestivalImagesInline(admin.TabularInline):
    model = Festival.images.through
    readonly_fields = ("preview",)
    verbose_name = "Изображение фестиваля"
    verbose_name_plural = "Изображения фестиваля"
    extra = 1
    classes = ["collapse"]

    def preview(self, obj):
        url = obj.image.image.url
        return format_html(f'<img src="{url}" width="200" height="100" style="object-fit: contain;" />')

    preview.short_description = "Превью"
    Festival.images.through.__str__ = lambda self: ""


@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ("year",)
    inlines = (
        VolunteerInline,
        FestivalImagesInline,
    )
    exclude = (
        "teams",
        "sponsors",
        "images",
    )
    empty_value_display = "-пусто-"


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "city",
        "address",
    )

    list_filter = ("city",)
    search_fields = ("name", "address")


@admin.register(PressRelease)
class PressReleaseAdmin(admin.ModelAdmin):
    list_display = ("festival",)
    list_filter = ("festival",)


class PressRealeaseAdmin(admin.ModelAdmin):
    list_display = ("title",)
    list_filter = ("title",)
    search_fields = ("title",)


@admin.register(ArtTeamMember)
class ArtTeamMemberAdmin(admin.ModelAdmin):
    form = ArtTeamMemberForm
    list_display = (
        "person",
        "team",
        "position",
        "is_pr_manager",
    )
    list_filter = ("is_pr_manager",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "person",
                    "position",
                    "is_pr_manager",
                ),
            },
        ),
        (
            None,
            {
                "fields": ("data_manager",),
                "classes": ("form-row field-data_manager",),
            },
        ),
    )

    ordering = ("person__last_name", "person__first_name")

    search_fields = ("position", "person__first_name", "person__last_name")

    def get_queryset(self, request):
        qs = self.model._default_manager.get_queryset().filter(team="art")
        return qs

    def save_model(self, request, obj, form, change):
        """Данные из поля 'data_manager' проверяются и сохраняются в модели 'Setting'."""
        if form.is_valid():
            team = "art"
            if obj.is_pr_manager:
                name_manager = form.cleaned_data["data_manager"]
                FestivalTeamMember.objects.filter(is_pr_manager=True).update(is_pr_manager=False)
                Setting.objects.filter(settings_key="pr_manager_name").update(text=name_manager)
            obj = form.save(commit=False)
            obj.team = team
            obj.save()
        else:
            raise ValidationError("Заполните поля корректно")

    class Media:
        """Adds a script that displays the field ```is_pr_manager``` if the team art is selected."""

        js = ("admin/info/js/FestivalTeamFooter.js",)


@admin.register(FestTeamMember)
class FestTeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        "person",
        "team",
        "position",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "person",
                    "position",
                ),
            },
        ),
    )

    ordering = ("person__last_name", "person__first_name")

    search_fields = ("position", "person__first_name", "person__last_name")

    def save_model(self, request, obj, form, change):
        """Устанваливается поле "team" на значение "fest"."""
        if form.is_valid():
            team = "fest"
            obj = form.save(commit=False)
            obj.team = team
            obj.save()
        else:
            raise ValidationError("Заполните поля корректно")

    def get_queryset(self, request):
        qs = self.model._default_manager.get_queryset().filter(team="fest")
        return qs


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = (
        "person",
        "position",
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "author_name", "author_email", "question", "sent")
    list_filter = ("sent",)

    def has_module_permission(self, request):
        if request.user.is_authenticated and (request.user.is_admin or request.user.is_superuser):
            return super().has_module_permission(request)
        return False
