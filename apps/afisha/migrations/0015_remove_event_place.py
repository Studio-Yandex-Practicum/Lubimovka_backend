# Generated by Django 3.2.13 on 2022-07-15 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('afisha', '0014_merge_20220713_1716'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='place',
        ),
    ]
