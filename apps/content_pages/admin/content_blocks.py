from adminsortable2.admin import SortableInlineAdminMixin
from django import forms
from django.contrib import admin

from apps.afisha.models import Event
from apps.content_pages.models import (
    ContentPersonRole,
    EventsBlock,
    ExtendedPerson,
    ImagesBlock,
    OrderedEvent,
    OrderedImage,
    OrderedPlay,
    OrderedVideo,
    PersonsBlock,
    PlaysBlock,
    VideosBlock,
)
from apps.content_pages.services import choices_for_blog_person
from apps.core.mixins import AdminImagePreview, HideOnNavPanelAdminModelMixin
from apps.core.models import Role
from apps.library.models import Play


class ContentPersonRoleInline(admin.TabularInline):
    model = ContentPersonRole
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Restricts role types for the model where inline is used."""
        if db_field.name == "role":
            kwargs["queryset"] = Role.objects.filter(types__role_type="blog_persons_role")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class OrderedInline(SortableInlineAdminMixin, admin.TabularInline):
    min_num = 1
    extra = 0


class OrderedEventInline(OrderedInline):
    model = OrderedEvent
    max_num = 3

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = Event.objects.filter(common_event__performance__isnull=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class OrderedImageInline(AdminImagePreview, OrderedInline):
    readonly_fields = ("image_preview_change_page",)
    model = OrderedImage
    max_num = 8


class OrderedVideoInline(OrderedInline):
    model = OrderedVideo


class OrderedPlayInline(OrderedInline):
    model = OrderedPlay
    autocomplete_fields = ("item",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = Play.objects.filter(other_play=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ExtendedPersonModelForm(forms.ModelForm):
    roles = forms.MultipleChoiceField(
        choices=choices_for_blog_person,
    )

    def get_initial_for_field(self, field, field_name):
        if self.instance.pk and field is self.fields["roles"]:
            return list(self.instance.roles.values_list("pk", flat=True))
        return super().get_initial_for_field(field, field_name)

    class Meta:
        model = ExtendedPerson
        fields = "__all__"


class ExtendedPersonInline(OrderedInline):
    model = ExtendedPerson
    form = ExtendedPersonModelForm
    show_change_link = True
    autocomplete_fields = ("person",)


@admin.register(ExtendedPerson)
class ExtendedPersonAdmin(HideOnNavPanelAdminModelMixin, admin.ModelAdmin):
    list_display = (
        "person",
        "block",
    )
    list_filter = (
        ("block", admin.RelatedOnlyFieldListFilter),
        ("person", admin.RelatedOnlyFieldListFilter),
    )
    search_fields = (
        "block",
        "person",
    )
    inlines = (ContentPersonRoleInline,)


@admin.register(ImagesBlock)
class ImagesBlockAdmin(HideOnNavPanelAdminModelMixin, admin.ModelAdmin):
    list_display = ("title",)
    inlines = (OrderedImageInline,)


@admin.register(EventsBlock)
class EventsBlockAdmin(HideOnNavPanelAdminModelMixin, admin.ModelAdmin):
    list_display = ("title",)
    inlines = (OrderedEventInline,)


@admin.register(PersonsBlock)
class PersonsBlockAdmin(HideOnNavPanelAdminModelMixin, admin.ModelAdmin):
    inlines = (ExtendedPersonInline,)


@admin.register(PlaysBlock)
class PlaysBlockAdmin(HideOnNavPanelAdminModelMixin, admin.ModelAdmin):
    inlines = (OrderedPlayInline,)


@admin.register(VideosBlock)
class VideosBlockAdmin(HideOnNavPanelAdminModelMixin, admin.ModelAdmin):
    inlines = (OrderedVideoInline,)
