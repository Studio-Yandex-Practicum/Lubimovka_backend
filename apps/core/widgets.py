from django.forms.widgets import Select


class FkSelect(Select):
    template_name = "admin/widgets/custom_foreign_key_select.html"

    class Media:
        js = ("js/admin/ForeignKeyLimitChange.js",)
