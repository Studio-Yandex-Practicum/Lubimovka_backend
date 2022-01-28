from django.db import migrations


def add_settings(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")
    Setting.objects.create(
        field_type="IMAGE",
        group="FIRST_SCREEN",
        settings_key="main_first_screen_image",
        image="core/2021-09-30_14.37.56.jpg",
        description="Изображение для первой страницы",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0030_auto_20220127_1720"),
    ]

    operations = [migrations.RunPython(add_settings)]
