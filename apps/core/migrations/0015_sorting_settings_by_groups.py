from django.db import migrations


def sort_by_group(apps, schema_editor):
    Setting = apps.get_model('core', 'Setting')
    group = {
        "EMAIL": "mail",
        "MAIN": "main",
        "FIRST_SCREEN": "first_screen",
        "GENERAL": "GENERAL"
    }
    setting_first_screen = Setting.objects.filter(
        settings_key__icontains=group['FIRST_SCREEN']
    ).all()
    for setting in setting_first_screen:
        setting.group = 'FIRST_SCREEN'
        setting.save()
    setting_main = Setting.objects.filter(
        settings_key__icontains=group['MAIN'],
        group='GENERAL'
    ).all()
    for setting in setting_main:
        setting.group = 'MAIN'
        setting.save()
    setting_email = Setting.objects.filter(
        settings_key__icontains=group['EMAIL'],
        group="GENERAL"
    ).all()
    for setting in setting_email:
        setting.group = 'EMAIL'
        setting.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20211204_1552'),
    ]

    operations = [
        migrations.RunPython(sort_by_group),
    ]
