# Generated by Django 3.2.13 on 2022-06-19 15:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0007_auto_20220531_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogitem',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='Создатель'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='newsitem',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='Создатель'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='Создатель'),
            preserve_default=False,
        ),
    ]