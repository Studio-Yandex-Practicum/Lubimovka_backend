from django.db import migrations


def add_settings(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    Setting.objects.create(
        field_type="BANNER",
        group="MAIN",
        settings_key="main_banner_1",
        url="https://lubimovks.url.ru",
        image="core/lubimovka.jpg",
        json={
            "title": "title",
            "description": "description",
            "button": "TICKETS"
        },
        description="Банер",
    )

    Setting.objects.create(
        field_type="BANNER",
        group="MAIN",
        settings_key="main_banner_2",
        url="https://lubimovka.url.ru",
        image="core/lubimovka.jpg",
        json={
            "title": "title",
            "description": "description",
            "button": "TICKETS"
        },
        description="Банер",
    )

    Setting.objects.create(
        field_type="BANNER",
        group="MAIN",
        settings_key="main_banner_3",
        url="https://lubimovka.url.ru",
        image="core/lubimovka.jpg",
        json={
            "title": "title",
            "description": "description",
            "button": "TICKETS"
        },
        description="Банер",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0022_auto_20211228_1318"),
    ]

    operations = [migrations.RunPython(add_settings)]
