# Generated by Django 3.2.23 on 2024-03-01 13:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0006_alter_question_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='participationapplicationfestival',
            name='nickname',
            field=models.CharField(blank=True, max_length=30, null=True, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='Псевдоним'),
        ),
    ]
