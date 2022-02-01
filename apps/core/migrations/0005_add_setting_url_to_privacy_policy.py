from django.db import migrations


def add_general_settings(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    Setting.objects.get_or_create(
        field_type="URL",
        group="GENERAL",
        settings_key="url_to_privacy_policy",
        url="privacy-policy",
        description="Ссылка на обработку персональных данных",
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_add_program'),
    ]

    operations = [
        migrations.RunPython(
            add_general_settings,
        ),
    ]
