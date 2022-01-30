import django.contrib.auth.validators
from django.db import migrations
import django.utils.timezone


def add_program(apps, schema_editor):
    Program = apps.get_model("library", "ProgramType")
    Program.objects.create(
        name="Внеконкурсная программа",
        slug="vnekonkursnaja-programma"
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_setting_initial_data'),
    ]

    operations = [
        migrations.RunPython(
            add_program,
        ),
    ]
