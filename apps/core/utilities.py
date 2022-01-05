import jsonschema
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify as django_slugify

from apps.core.constants import ALPHABET

BANNER_SCHEMA = {
    "type": "object",
    "title": "json",
    "minProperties": 3,
    "maxProperties": 3,
    "properties": {
        "title": {"type": "string", "maxLength": 100},
        "description": {"type": "string", "maxLength": 500},
        "button": {"type": "string", "maxLength": 100, "pattern": "^TICKETS$|^READ$|^DETAILS$"},
    },
    "required": ["title"],
}

BASE_SCHEMA = {
    "type": "object",
    "title": "json",
    "minProperties": 0,
    "maxProperties": 5,
}


def slugify(name):
    return django_slugify("".join(ALPHABET.get(char, char) for char in name.lower()))


def validate_json_field(setting, schema, text_error):
    try:
        jsonschema.validate(setting.json, schema)
    except jsonschema.exceptions.ValidationError as e:
        raise ValidationError(f"{text_error} ({e.message})")


def check_json_field(setting):
    if setting.field_type == setting.SettingFieldType.BANNER:
        validate_json_field(setting, BANNER_SCHEMA, "Необходимо правильно заполнить поля title, description, BUTTON")
    else:
        validate_json_field(setting, BASE_SCHEMA, "Некорректно наполнено поле json")
