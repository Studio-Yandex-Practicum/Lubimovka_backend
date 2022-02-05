from django.db import migrations


def add_press_release_setting(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    Setting.objects.create(
        field_type="TEXT",
        group="GENERAL",
        settings_key="press_release_data",
        text="По вопросам PR и аккредитации пишите Анне Загородниковой",
        description="Данные о PR-менеджере на странице для прессы",
    )
    Setting.objects.create(
        field_type="IMAGE",
        group="GENERAL",
        settings_key="press_release_image",
        image="core/2021-09-30_14.37.56.jpg",
        description="Фото PR-менеджера на странице для прессы",
    )
    Setting.objects.create(
        field_type="EMAIL",
        group="GENERAL",
        settings_key="press_release_email",
        email="annaszagorodnikova@gmail.com",
        description="Почта PR-менеджера на странице для прессы",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_facebook_photo_gallery_link"),
    ]

    operations = [
        migrations.RunPython(
            add_press_release_setting,
        ),
    ]
