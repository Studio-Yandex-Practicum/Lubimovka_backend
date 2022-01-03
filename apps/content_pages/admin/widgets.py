from django.forms.widgets import HiddenInput, Select


class CustomHiddenInput(HiddenInput):
    template_name = "admin/widgets/custom_hidden.html"


class CustomSelect(Select):
    template_name = "admin/widgets/custom_select.html"

    class Media:
        js = ("content-pages/admin/genericForeignKeyAddChange.js",)
