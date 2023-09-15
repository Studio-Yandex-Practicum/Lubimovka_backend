# Generated by Django 3.2.20 on 2023-09-13 09:35

from django.db import migrations

SHOW_TEAM_SETTING = "show_team"
SHOW_SPONSORS_SETTING = "show_sponsors"
SHOW_VOLUNTEERS_SETTING = "show_volunteers"


def add_settings(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    Setting.objects.get_or_create(
        field_type="BOOLEAN",
        group="GENERAL",
        settings_key=SHOW_TEAM_SETTING,
        boolean=False,
        description="Отображать организаторов",
    )
    Setting.objects.get_or_create(
        field_type="BOOLEAN",
        group="GENERAL",
        settings_key=SHOW_SPONSORS_SETTING,
        boolean=False,
        description="Отображать попечителей",
    )
    Setting.objects.get_or_create(
        field_type="BOOLEAN",
        group="GENERAL",
        settings_key=SHOW_VOLUNTEERS_SETTING,
        boolean=False,
        description="Отображать волонтеров",
    )

def remove_settings(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    Setting.objects.filter(
        settings_key__in=(
            SHOW_TEAM_SETTING, SHOW_SPONSORS_SETTING, SHOW_VOLUNTEERS_SETTING
        )
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_alter_roletype_role_type'),
    ]

    operations = [
        migrations.RunPython(code=add_settings, reverse_code=remove_settings)
    ]
