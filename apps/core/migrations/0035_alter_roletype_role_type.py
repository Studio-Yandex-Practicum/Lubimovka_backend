# Generated by Django 3.2.18 on 2023-05-17 14:54

from django.db import migrations, models
from django.db.models import Exists, OuterRef

MASTERCLASS_ROLE = "master_class_role"
READING_ROLE = "reading_role"


def merge_masterclass_roles_to_readings(apps, schema_editor):
    RoleType = apps.get_model("core", "RoleType")
    masterclass_roletype = RoleType.objects.filter(role_type=MASTERCLASS_ROLE).first()
    reading_roletype = RoleType.objects.filter(role_type=READING_ROLE).first()
    if masterclass_roletype and reading_roletype:
        Through = apps.get_model("core", "Role").types.through
        same_roles = Through.objects.filter(roletype=reading_roletype, role=OuterRef("role"))
        Through.objects.filter(~Exists(same_roles), roletype=masterclass_roletype).update(roletype=reading_roletype)
        Through.objects.filter(roletype=masterclass_roletype).delete()
    RoleType.objects.filter(role_type=MASTERCLASS_ROLE).delete()


def restore_roles_in_masterclass(apps, schema_editor):
    RoleType = apps.get_model("core", "RoleType")
    RoleType.objects.get_or_create(role_type=MASTERCLASS_ROLE)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_update_questions_field_type'),
    ]

    operations = [
        migrations.RunPython(merge_masterclass_roles_to_readings, restore_roles_in_masterclass),
        migrations.AlterField(
            model_name='roletype',
            name='role_type',
            field=models.CharField(choices=[('blog_persons_role', 'Роль в блоге'), ('performanse_role', 'Роль в спектаклях'), ('play_role', 'Роль в пьесах'), ('reading_role', 'Роль в специальных событиях')], default='blog_persons_role', help_text='Укажите, где будет использована роль', max_length=20, unique=True, verbose_name='Тип роли'),
        ),
    ]