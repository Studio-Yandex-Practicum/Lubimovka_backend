# Generated by Django 3.2.9 on 2021-11-18 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_add_and_fix_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='description',
            field=models.CharField(max_length=60, null=True, verbose_name='Описание настройки'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='settings_key',
            field=models.SlugField(max_length=40, unique=True, verbose_name='Ключ настройки'),
        ),
    ]
