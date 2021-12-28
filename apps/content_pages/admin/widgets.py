# Some sort of modification of the `django-gfklookupwidget`
# https://github.com/mqsoh/django-gfklookupwidget

from typing import Any, Dict, Optional

from django.contrib.contenttypes.models import ContentType
from django.forms.widgets import NumberInput, Select
from django.urls import NoReverseMatch, reverse

POPUP_TYPE_ADD = "add"
POPUP_TYPE_CHANGE = "change"
POPUP_SUFFIX = "?_popup=1"


class CustomSelect(Select):
    template_name = "admin/widgets/custom_select.html"

    def get_context(self, name: str, value: Any, attrs: Optional[Any]) -> Dict[str, Any]:
        context = super().get_context(name, value, attrs)
        context["value"] = value
        return context


class GfkPopupWidget(NumberInput):
    """Provide a link to add or edit GenericForeignKeys related object.

    It's a wad of JavaScript that inspects the select box generated for the
    contenttypes framework's content_type field and uses Django's normal
    showRelatedObjectPopup to populate the text field represented by this
    widget.
    """

    template_name = "admin/widgets/generic_foreign_key_widget.html"

    class Media:
        js = ("content-pages/admin/genericForeignKeyPopupOnClick.js",)

    def __init__(self, *args, **kwargs):
        """Set required for widget args.

        Args:
            - content_type_field_name: This is name of the field that becomes a select box in the admin.
            - parent_class: This is a model class.
        """
        self.content_type_field_name = kwargs.pop("content_type_field_name")
        self.parent_class = kwargs.pop("parent_class")
        super().__init__(*args, **kwargs)

    def get_context(self, name: str, value: Any, attrs: Optional[Any]) -> Dict[str, Any]:
        popup_type, urls = self._prepare_context(value)
        urls_id = name + "_urls"

        extended_context = {
            "content_type_field_name": self.content_type_field_name,
            "popup_type": popup_type,
            "urls": urls,
            "urls_id": urls_id,
        }

        context = super().get_context(name, value, attrs)
        context.update(extended_context)
        return context

    def _prepare_context(self, value):
        content_type_field = self.parent_class._meta.get_field(self.content_type_field_name)
        choices = content_type_field.get_choices()

        # Generate an ID to Content Type lookup dict now so we don't have to
        # perform multiple queries in the for-loop below.
        content_types_lookup = {
            content_type.id: content_type
            for content_type in ContentType.objects.filter(id__in=[ct_id for ct_id, _ in choices if ct_id])
        }

        popup_type = POPUP_TYPE_CHANGE
        url_args = (value,)

        # When default value is None, input box should be empty and `add` action instead of `change`.
        # `url_args` should be empty for `add` action.
        if value is None:
            value = ""
            popup_type = POPUP_TYPE_ADD
            url_args = None

        # We'll generate the URLs for each supported content type upfront and
        # store them in a dict indexed on the model name. This will allow the
        # JavaScript to get the URL based on the <select> box markup.
        urls = {}
        for type_id, _ in choices:
            # This is the default "-------" entry.
            if not type_id:
                continue

            content_type = content_types_lookup[type_id]

            # The URLs for the anchors used by showRelatedObjectPopup
            # have the form of:
            #     /<app_label>/<model>/add/?_popup=1
            #     or
            #     /<app_label>/<model>/<id>/change/?_popup=1
            try:
                url = reverse(f"admin:{content_type.app_label}_{content_type.model}_{popup_type}", args=url_args)
                url += POPUP_SUFFIX

            except NoReverseMatch:
                # This content type isn't available in the admin, so we can't
                # provide the popup. This is common, so we'll just ignore this
                # one.
                continue

            urls[type_id] = url

        return popup_type, urls
