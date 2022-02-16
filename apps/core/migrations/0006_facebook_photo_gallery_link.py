from django.db import migrations


def add_general_settings(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    Setting.objects.get_or_create(
        field_type="URL",
        group="GENERAL",
        settings_key="photo_gallery_facebook",
        url="https://www.facebook.com/festival.lubimovka/photos",
        description="Ссылка на фотоальбомы в Facebook на странице для прессы",
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_add_setting_url_to_privacy_policy'),
    ]

    operations = [
        migrations.RunPython(
            add_general_settings,
        ),
    ]
