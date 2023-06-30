# Generated by Django 3.2.18 on 2023-05-30 00:11

from django.db import migrations


def merge_masterclass_to_reading(apps, schema_editor):
    Event = apps.get_model("afisha", "Event")
    Event.objects.filter(type="MASTERCLASS").update(type="READING")

    MasterClass = apps.get_model("afisha", "MasterClass")
    Reading = apps.get_model("afisha", "Reading")

    for masterclass in MasterClass.objects.all():
        team_members = masterclass.team_members.all()
        reading = Reading.objects.create(
            play = None,
            name = masterclass.name,
            description = masterclass.description,
            events = masterclass.events,
            main_image = masterclass.main_image,
            intro = masterclass.intro
        )
        for team_member in team_members:
            team_member.masterclass = None
            team_member.reading = reading
            team_member.save()
        masterclass.delete()


def extract_masterclass_from_reading(apps, schema_editor):
    MasterClass = apps.get_model("afisha", "MasterClass")
    Reading = apps.get_model("afisha", "Reading")
    for reading in Reading.objects.filter(play__isnull=True):
        team_members = reading.team_members.all()
        masterclass = MasterClass.objects.create(
            name = reading.name,
            description = reading.description,
            events = reading.events,
            main_image = reading.main_image,
            intro = reading.intro
        )
        event = masterclass.events
        event.type = "MASTERCLASS"
        event.save()
        for team_member in team_members:
            team_member.masterclass = masterclass
            team_member.reading = None
            team_member.save()
        reading.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('afisha', '0027_auto_20230530_0309'),
    ]

    operations = [
        migrations.RunPython(merge_masterclass_to_reading, extract_masterclass_from_reading),
    ]