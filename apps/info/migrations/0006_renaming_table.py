from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '005_festivalteam_is_pr_manager'),
    ]

    operations = [
        migrations.RenameModel("FestivalTeam", "FestivalTeamMember")
    ]
