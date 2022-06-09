from django.db import migrations


def change_email_settings(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    values_for_update_email_send_from = {"text": "admin@lubimovka.ru"}
    Setting.objects.update_or_create(
        settings_key="email_send_from",
        defaults=values_for_update_email_send_from,
    )

class Migration(migrations.Migration):
    dependencies = [
        ("core", "0020_alter_person_email"),
    ]

    operations = [
        migrations.RunPython(
            change_email_settings,
        ),
    ]
