# Generated by Django 5.1.2 on 2024-11-05 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0035_alter_player_scores'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='scores',
            new_name='league_scores',
        ),
    ]
