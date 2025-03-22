# Generated by Django 4.2.5 on 2023-12-08 13:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0003_alter_team_options_alter_playermembership_team"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="game_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("best-ball", "Best Ball"),
                    ("stroke", "Stroke"),
                    ("skins", "Skins"),
                    ("stroke-skins", "Stroke w/Skins"),
                ],
                default=None,
                max_length=32,
                null=True,
            ),
        ),
    ]
