from django.db import migrations


def add_general_settings(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    values_for_site_color = {
        "settings_key": "background_color",
        "text": "#ECEBE8",
        "description": "Цвет основного фона сайта",
    }
    values_for_pr_director_name = {
        "description": "Имя PR директора на странице для прессы (в дательном падеже)"
    }
    Setting.objects.update_or_create(
        settings_key="site_color",
        defaults=values_for_site_color,
    )
    Setting.objects.create(
        field_type="TEXT",
        group="GENERAL",
        settings_key="accent_color",
        text="#B7C09D",
        description="Цвет акцента сайта",
    )
    Setting.objects.update_or_create(
        settings_key="pr_director_name",
        defaults=values_for_pr_director_name,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_alter_person_city'),
    ]

    operations = [
        migrations.RunPython(
            add_general_settings,
        ),
    ]
