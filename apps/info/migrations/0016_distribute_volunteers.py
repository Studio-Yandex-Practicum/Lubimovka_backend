from django.db import migrations
import random

def distribute_volunteers_to_festivals(apps, schema_editor):
    Volunteer = apps.get_model("info", "Volunteer")
    Festival = apps.get_model("info", "Festival")

    festivals = list(Festival.objects.all())

    for obj in Volunteer.objects.all():
        obj.festival = random.choice(festivals)
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0015_auto_20220121_1138'),
    ]

    operations = [
        migrations.RunPython(distribute_volunteers_to_festivals),
    ]
