# Generated by Django 3.2.16 on 2022-12-03 22:25

from django.db import migrations, models


def expand_programs(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Play = apps.get_model('library', 'Play')
    for play in Play.objects.all():
        program = play.program
        if program:
            play.programs.add(program)
            play.save()


def shrink_programs(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Play = apps.get_model('library', 'Play')
    for play in Play.objects.all():
        play.program = play.programs.first()
        play.save()


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0038_auto_20220817_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='play',
            name='programs',
            field=models.ManyToManyField(help_text='Для пьес Любимовки должна быть выбрана хотя бы одна Программа.', related_name='plays', to='library.ProgramType', verbose_name='Программа'),
        ),
        migrations.RunPython(expand_programs, shrink_programs),
        migrations.RemoveField(
            model_name='play',
            name='program',
        ),
    ]
