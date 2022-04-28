from django import forms
from django.conf import settings
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS, AutocompleteSelect
from django.forms.widgets import Select
from django.utils.translation import get_language


class FkSelect(Select):
    template_name = "admin/widgets/custom_foreign_key_select.html"

    class Media:
        js = ("js/admin/ForeignKeyLimitChange.js",)


class AutocompleteSelectWithRestriction(AutocompleteSelect):
    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        attrs.update(
            {
                "class": attrs["class"] + (" " if attrs["class"] else "") + "foreign-key-field",
            }
        )
        return attrs

    @property
    def media(self):
        extra = "" if settings.DEBUG else ".min"
        i18n_name = SELECT2_TRANSLATIONS.get(get_language())
        i18n_file = ("admin/js/vendor/select2/i18n/%s.js" % i18n_name,) if i18n_name else ()
        return forms.Media(
            js=(
                "admin/js/vendor/jquery/jquery%s.js" % extra,
                "admin/js/vendor/select2/select2.full%s.js" % extra,
            )
            + i18n_file
            + (
                "admin/js/jquery.init.js",
                "admin/js/autocomplete.js",
            )
            + ("js/admin/ForeignKeyLimitChange.js",),
            css={
                "screen": (
                    "admin/css/vendor/select2/select2%s.css" % extra,
                    "admin/css/autocomplete.css",
                ),
            },
        )
