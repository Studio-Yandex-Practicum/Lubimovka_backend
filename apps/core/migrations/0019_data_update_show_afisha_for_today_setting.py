from django.db import migrations, models

def change_email_settings(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    values_for_update_setting = {"description": "Отображение афиши только на сегодня (в противном случае " "отображаются ближайшие 6 событий)",}
    Setting.objects.update_or_create(
        settings_key="main_show_afisha_only_for_today",
        defaults=values_for_update_setting,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_person_email'),
    ]

    operations = [
        migrations.RunPython(
            change_email_settings,
        ),
    ]
