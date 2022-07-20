from xmlrpc.client import boolean
from django.db import migrations


def setting_for_partner_block(apps, schema_editor):

    Setting = apps.get_model("core", "Setting")

    Setting.objects.get_or_create(
        field_type="BOOLEAN",
        group="GENERAL",
        settings_key="partner_block_on_main_and_festival_pages",
        boolean=True,
        description="Отображать блок партнёров на главной и странице о фестивале",
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
