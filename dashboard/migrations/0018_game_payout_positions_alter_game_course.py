# Generated by Django 4.2.5 on 2024-03-06 02:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0017_game_use_teams_alter_game_game_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="payout_positions",
            field=models.PositiveSmallIntegerField(
                choices=[(1, " 1"), (2, " 2"), (3, " 3")], default=1
            ),
        ),
        migrations.AlterField(
            model_name="game",
            name="course",
            field=models.ForeignKey(
                default=2,
                on_delete=django.db.models.deletion.PROTECT,
                to="dashboard.golfcourse",
            ),
        ),
    ]
