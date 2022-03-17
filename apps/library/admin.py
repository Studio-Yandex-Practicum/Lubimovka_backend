from django.contrib import admin
from django.contrib.sites.models import Site

from apps.core.mixins import InlineReadOnlyMixin, StatusButtonMixin
from apps.core.models import Person, Role
from apps.library.forms.admin import AuthorForm
from apps.library.models import (
    Achievement,
    Author,
    MasterClass,
    OtherLink,
    OtherPlay,
    ParticipationApplicationFestival,
    Performance,
    PerformanceMediaReview,
    PerformanceReview,
    Play,
    ProgramType,
    Reading,
    SocialNetworkLink,
    TeamMember,
)


class AuthorInline(admin.TabularInline):
    model = Author.plays.through
    # extra = 0
    min_num = 1
    verbose_name = "Автор"
    verbose_name_plural = "Авторы"
    classes = ["collapse"]


class PlayAdmin(admin.ModelAdmin):
    filter_horizontal = ("authors",)
    list_display = (
        "name",
        "city",
        "program",
        "festival",
        "published",
    )
    inlines = (AuthorInline,)
    list_filter = (
        "authors",
        "city",
        "program",
        "festival",
        "published",
    )
    search_fields = (
        "authors__person__first_name",
        "authors__person__last_name",
        "name",
        "city",
        "program__name",
        "festival__year",
    )
    fields = (
        "name",
        "city",
        "year",
        "url_download",
        "url_reading",
        "program",
        "festival",
        "published",
    )


class AchievementAdmin(admin.ModelAdmin):
    list_display = ("tag",)


class AchievementInline(admin.TabularInline):
    model = Author.achievements.through
    extra = 1
    verbose_name = "Достижение"
    verbose_name_plural = "Достижения"
    classes = ["collapse"]


class PlayInline(admin.TabularInline):
    model = Author.plays.through
    extra = 1
    verbose_name = "Пьеса"
    verbose_name_plural = "Пьесы"
    classes = ["collapse"]


class SocialNetworkLinkInline(admin.TabularInline):
    model = SocialNetworkLink
    extra = 1
    classes = ["collapse"]


class OtherLinkInline(admin.TabularInline):
    model = OtherLink
    extra = 1
    classes = ["collapse"]


class OtherPlayInline(admin.StackedInline):
    model = OtherPlay
    extra = 1


class AuthorAdmin(admin.ModelAdmin):
    form = AuthorForm
    list_display = (
        "person",
        "quote",
        "biography",
        "slug",
    )
    inlines = (
        AchievementInline,
        PlayInline,
        SocialNetworkLinkInline,
        OtherLinkInline,
        OtherPlayInline,
    )
    exclude = (
        "achievements",
        "plays",
        "social_network_links",
        "other_links",
        "other_plays_links",
    )
    list_filter = ("achievements",)
    search_fields = (
        "biography",
        "slug",
        "person__first_name",
        "person__last_name",
        "person__middle_name",
        "person__email",
    )
    empty_value_display = "-пусто-"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm("library.can_change_author"):
            return form
        if obj:
            form.base_fields["person"].queryset = Person.objects.exclude(authors__in=Author.objects.exclude(id=obj.id))
        else:
            form.base_fields["person"].queryset = Person.objects.exclude(authors__in=Author.objects.all())
        return form


class PerformanceMediaReviewAdmin(admin.ModelAdmin):
    list_display = (
        "media_name",
        "performance",
        "pub_date",
    )
    list_filter = (
        "media_name",
        "performance__name",
        "pub_date",
    )
    search_fields = (
        "media_name",
        "performance__name",
        "pub_date",
    )
    readonly_fields = ("pub_date",)


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
    search_fields = (
        "reviewer_name",
        "performance__name",
        "pub_date",
    )
    readonly_fields = ("pub_date",)


class ProgramTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)

    def get_readonly_fields(self, request, obj=None):
        """Only superusers can edit slug field."""
        if not request.user.is_superuser:
            return ("slug",)
        return super().get_readonly_fields(request, obj)


class PerformanceReviewInline(InlineReadOnlyMixin, admin.TabularInline):
    model = PerformanceReview
    extra = 0
    max_num = 8
    classes = ["collapse"]


class PerformanceMediaReviewInline(InlineReadOnlyMixin, admin.TabularInline):
    model = PerformanceMediaReview
    extra = 0
    max_num = 8
    classes = ["collapse"]


class TeamMemberInline(InlineReadOnlyMixin, admin.TabularInline):
    model = TeamMember
    fields = (
        "person",
        "role",
    )
    extra = 0
    classes = ["collapse"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Restricts role types for the model where inline is used."""
        LIMIT_ROLES = {
            Performance: "performanse_role",
            Play: "play_role",
            MasterClass: "master_class_role",
            Reading: "reading_role",
        }
        if db_field.name == "role":
            if self.parent_model in LIMIT_ROLES.keys():
                kwargs["queryset"] = Role.objects.filter(types__role_type=LIMIT_ROLES[self.parent_model])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ImagesInBlockInline(InlineReadOnlyMixin, admin.TabularInline):
    model = Performance.images_in_block.through
    verbose_name = "Изображение в блоке изображений"
    verbose_name_plural = "Изображения в блоке изображений"
    extra = 0
    max_num = 8
    classes = ["collapse"]


class PerformanceAdmin(StatusButtonMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "play",
        "status",
    )
    fields = (
        "status",
        "name",
        "play",
        "main_image",
        "bottom_image",
        "video",
        "description",
        "text",
        "age_limit",
        "project",
        "duration",
    )
    list_filter = (
        "age_limit",
        "status",
    )
    search_fields = (
        "play__name",
        "name",
        "text",
    )
    readonly_fields = ("status",)
    other_readonly_fields = (
        "status",
        "name",
        "play",
        "main_image",
        "bottom_image",
        "video",
        "description",
        "text",
        "age_limit",
        "project",
        "duration",
    )
    inlines = (
        ImagesInBlockInline,
        PerformanceReviewInline,
        PerformanceMediaReviewInline,
        TeamMemberInline,
    )


class ReadingAdmin(admin.ModelAdmin):
    list_display = (
        "play",
        "name",
    )
    exclude = ("events",)
    search_fields = (
        "play__name",
        "name",
    )
    inlines = (TeamMemberInline,)


class MasterClassAdmin(admin.ModelAdmin):
    list_display = ("name",)
    exclude = ("events",)
    search_fields = (
        "play__name",
        "name",
    )
    inlines = (TeamMemberInline,)


class ParticipationAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "first_name",
        "last_name",
        "year",
        "verified",
        "exported_to_google",
        "saved_to_storage",
    )
    list_filter = (
        "year",
        "verified",
        "city",
    )
    search_fields = (
        "title",
        "first_name",
        "last_name",
        "city",
        "year",
    )


admin.site.register(Play, PlayAdmin)
admin.site.register(Performance, PerformanceAdmin)
admin.site.register(Achievement, AchievementAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(PerformanceMediaReview, PerformanceMediaReviewAdmin)
admin.site.register(PerformanceReview, PerformanceReviewAdmin)
admin.site.register(ParticipationApplicationFestival, ParticipationAdmin)
admin.site.register(Reading, ReadingAdmin)
admin.site.register(MasterClass, MasterClassAdmin)
admin.site.register(ProgramType, ProgramTypeAdmin)
admin.site.unregister(Site)
