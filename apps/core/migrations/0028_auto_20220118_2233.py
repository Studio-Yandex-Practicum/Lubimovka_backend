# Generated by Django 3.2.10 on 2022-01-18 22:33

import apps.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_add_afisha_settings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='first_name',
            field=models.CharField(max_length=50, validators=[apps.core.validators.name_validator], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='person',
            name='last_name',
            field=models.CharField(max_length=50, validators=[apps.core.validators.name_validator], verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='person',
            name='middle_name',
            field=models.CharField(blank=True, max_length=50, validators=[apps.core.validators.name_validator], verbose_name='Отчество'),
        ),
    ]
