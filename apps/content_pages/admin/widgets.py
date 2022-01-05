from django.forms.widgets import HiddenInput, Select


class GfkHiddenInput(HiddenInput):
    template_name = "admin/widgets/custom_hidden.html"


class GfkSelect(Select):
    template_name = "admin/widgets/custom_select.html"

    class Media:
        js = ("content-pages/admin/genericForeignKeyAddChange.js",)
