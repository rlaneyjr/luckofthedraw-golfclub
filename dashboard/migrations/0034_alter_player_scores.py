# Generated by Django 5.1.2 on 2024-11-02 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0033_player_scores'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='scores',
            field=models.JSONField(default=list),
        ),
    ]
