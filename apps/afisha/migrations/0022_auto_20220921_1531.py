# Generated by Django 3.2.13 on 2022-09-21 12:31

from django.db import migrations, models


def make_hidden(apps, schema_editor):
    Event = apps.get_model("afisha", "Event")
    Event.objects.update(hidden_on_main=models.Q(pinned_on_main=False))


def make_pinned(apps, schema_editor):
    Event = apps.get_model("afisha", "Event")
    Event.objects.update(pinned_on_main=models.Q(hidden_on_main=False))


class Migration(migrations.Migration):

    dependencies = [
        ('afisha', '0021_event_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='hidden_on_main',
            field=models.BooleanField(default=True, verbose_name='Скрыть на главной'),
        ),
        migrations.RunPython(make_hidden, make_pinned),
        migrations.RemoveField(
            model_name='event',
            name='pinned_on_main',
        ),
    ]
