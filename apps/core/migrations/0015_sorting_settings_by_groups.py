from django.db import migrations


def sort_by_groupe(apps, schema_editor):
    Settings = apps.get_model('core', 'Settings')
    group = {
        "EMAIL": "mail",
        "MAIN": "main",
        "FIRST_SCREEN": "first_screen",
        "GENERAL": "GENERAL"
    }
    settings_first_screen = Settings.objects.filter(
        settings_key__icontains=group['FIRST_SCREEN']
    ).all()
    for setting in settings_first_screen:
        setting.group = 'FIRST_SCREEN'
        setting.save()
    settings_main = Settings.objects.filter(
        settings_key__icontains=group['MAIN'],
        group='GENERAL'
    ).all()
    for setting in settings_main:
        setting.group = 'MAIN'
        setting.save()
    settings_email = Settings.objects.filter(
        settings_key__icontains=group['EMAIL'],
        group="GENERAL"
    ).all()
    for setting in settings_email:
        setting.group = 'EMAIL'
        setting.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20211204_1552'),
    ]

    operations = [
        migrations.RunPython(sort_by_groupe),
    ]
