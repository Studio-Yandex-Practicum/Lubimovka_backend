from django.db import migrations


def update_field_type(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    Setting.objects.filter(settings_key="email_to_send_questions").update(
        field_type="EMAIL",
        group="EMAIL",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0033_rename_email_settings"),
    ]

    operations = [
        migrations.RunPython(
            update_field_type, migrations.RunPython.noop
        ),
    ]
