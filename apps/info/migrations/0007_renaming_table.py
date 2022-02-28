from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0006_alter_partner_image'),
    ]

    operations = [
        migrations.RenameModel("FestivalTeam", "FestivalTeamMember")
    ]
