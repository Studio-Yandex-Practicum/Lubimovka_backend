from django.db import migrations


def change_email_settings(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    # removing email_question_template_id
    Setting.objects.filter(
        field_type="TEXT",
        group="EMAIL",
        settings_key="email_question_template_id",
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0013_ordering_of_people'),
    ]

    operations = [
        migrations.RunPython(
            change_email_settings,
        ),
    ]
