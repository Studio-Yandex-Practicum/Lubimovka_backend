# Generated by Django 3.2.13 on 2022-08-07 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0025_auto_20220730_0909'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('info.volunteer',),
        ),
    ]
