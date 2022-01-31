from django.db import migrations


def add_program(apps, schema_editor):
    Program = apps.get_model("library", "ProgramType")
    Program.objects.create(
        name="Внеконкурсная программа",
        slug="vnekonkursnaja-programma"
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_image_in_blog_reqired'),
    ]

    operations = [
        migrations.RunPython(
            add_program,
        ),
    ]
