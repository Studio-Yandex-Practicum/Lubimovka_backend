from django.template.defaultfilters import slugify as django_slugify

from apps.core.constants import ALPHABET


def slugify(name):
    return django_slugify("".join(ALPHABET.get(char, char) for char in name.lower()))


def turn_off_setting(switchable_setting):
    from apps.core.models import Setting

    if Setting.objects.filter(settings_key=switchable_setting).exists():
        main_add_news_setting = Setting.objects.get(settings_key=switchable_setting)
        main_add_news_setting.boolean = False
        main_add_news_setting.save()


def check_related_settings(setting):
    related_settings = {
        "main_add_blog": "main_add_news",
        "main_add_news": "main_add_blog",
    }
    for enable_setting, switchable_setting in related_settings.items():
        if setting.settings_key == enable_setting and setting.boolean is True:
            turn_off_setting(switchable_setting)
