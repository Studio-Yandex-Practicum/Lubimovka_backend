# Generated by Django 3.2.12 on 2022-03-15 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0010_auto_20220314_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtTeamMember',
            fields=[
            ],
            options={
                'verbose_name': 'Арт-дирекция фестиваля',
                'verbose_name_plural': 'Арт-дирекция фестиваля',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('info.festivalteammember',),
        ),
        migrations.CreateModel(
            name='FestTeamMember',
            fields=[
            ],
            options={
                'verbose_name': 'Команда фестиваля',
                'verbose_name_plural': 'Команда фестиваля',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('info.festivalteammember',),
        ),
    ]
