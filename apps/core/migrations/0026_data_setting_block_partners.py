from django.db import migrations


def setting_for_partner_block(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    Setting.objects.get_or_create(
        field_type="BOOLEAN",
        group="GENERAL",
        settings_key="show_general_partners",
        boolean=True,
        description="Отображать генеральных партнёров",
    )
    Setting.objects.get_or_create(
        field_type="BOOLEAN",
        group="GENERAL",
        settings_key="show_info_partners_and_festival_partners",
        boolean=True,
        description="Отображать информационных партнёров и партнёров фестиваля",
    )

class Migration(migrations.Migration):
    dependencies = [
        ("core", "0025_alter_role_slug"),
    ]

    operations = [
        migrations.RunPython(
            setting_for_partner_block,
        ),
    ]
