from django.db import migrations


def add_settings(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    Setting.objects.filter(settings_key="main_afisha_title").delete()
    Setting.objects.filter(settings_key="main_afisha_description").delete()
    Setting.objects.filter(settings_key="main_afisha_button_label").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0025_alter_setting_group"),
    ]

    operations = [migrations.RunPython(add_settings)]
