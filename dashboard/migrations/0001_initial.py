# Generated by Django 4.2.5 on 2023-12-05 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Game",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "game_type",
                    models.CharField(
                        choices=[
                            ("best-ball", "Best Ball"),
                            ("stroke", "Stroke"),
                            ("skins", "Skins"),
                            ("stroke-skins", "Stroke w/Skins"),
                        ],
                        default="stroke",
                        max_length=32,
                    ),
                ),
                ("date_played", models.DateTimeField(blank=True, null=True)),
                (
                    "holes_played",
                    models.PositiveSmallIntegerField(
                        choices=[(9, "9 Holes"), (18, "18 Holes")], default=18
                    ),
                ),
                (
                    "which_holes",
                    models.CharField(
                        choices=[
                            ("all", "All"),
                            ("front", "Front 9"),
                            ("back", "Back 9"),
                        ],
                        default="all",
                        max_length=5,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("setup", "Setup"),
                            ("active", "Active"),
                            ("completed", "Completed"),
                            ("not_finished", "Not Finished"),
                        ],
                        default="setup",
                        max_length=64,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "games",
                "ordering": ["date_played", "status"],
            },
        ),
        migrations.CreateModel(
            name="GolfCourse",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128)),
                (
                    "initials",
                    models.CharField(
                        default="GC", max_length=5, verbose_name="Course Initials"
                    ),
                ),
                (
                    "hole_count",
                    models.PositiveSmallIntegerField(
                        choices=[(9, "9 Holes"), (18, "18 Holes")], default=18
                    ),
                ),
                ("tee_time_link", models.URLField(blank=True)),
                ("website_link", models.URLField(blank=True)),
                ("city", models.CharField(blank=True, max_length=128)),
                ("state", models.CharField(blank=True, max_length=64)),
                ("zip_code", models.CharField(blank=True, max_length=128)),
                (
                    "card",
                    models.ImageField(
                        blank=True, default=None, null=True, upload_to="images"
                    ),
                ),
                (
                    "overview",
                    models.ImageField(
                        blank=True, default=None, null=True, upload_to="images"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Hole",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("Hole1", "Hole 1"),
                            ("Hole2", "Hole 2"),
                            ("Hole3", "Hole 3"),
                            ("Hole4", "Hole 4"),
                            ("Hole5", "Hole 5"),
                            ("Hole6", "Hole 6"),
                            ("Hole7", "Hole 7"),
                            ("Hole8", "Hole 8"),
                            ("Hole9", "Hole 9"),
                            ("Hole10", "Hole 10"),
                            ("Hole11", "Hole 11"),
                            ("Hole12", "Hole 12"),
                            ("Hole13", "Hole 13"),
                            ("Hole14", "Hole 14"),
                            ("Hole15", "Hole 15"),
                            ("Hole16", "Hole 16"),
                            ("Hole17", "Hole 17"),
                            ("Hole18", "Hole 18"),
                        ],
                        default="Hole1",
                        max_length=7,
                    ),
                ),
                ("nickname", models.CharField(blank=True, max_length=64)),
                (
                    "par",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        choices=[(3, "Par 3"), (4, "Par 4"), (5, "Par 5")],
                        default=4,
                    ),
                ),
                (
                    "order",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        choices=[
                            (1, " 1"),
                            (2, " 2"),
                            (3, " 3"),
                            (4, " 4"),
                            (5, " 5"),
                            (6, " 6"),
                            (7, " 7"),
                            (8, " 8"),
                            (9, " 9"),
                            (10, " 10"),
                            (11, " 11"),
                            (12, " 12"),
                            (13, " 13"),
                            (14, " 14"),
                            (15, " 15"),
                            (16, " 16"),
                            (17, " 17"),
                            (18, " 18"),
                        ],
                        default=1,
                    ),
                ),
                (
                    "handicap",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        choices=[
                            (1, " 1"),
                            (2, " 2"),
                            (3, " 3"),
                            (4, " 4"),
                            (5, " 5"),
                            (6, " 6"),
                            (7, " 7"),
                            (8, " 8"),
                            (9, " 9"),
                            (10, " 10"),
                            (11, " 11"),
                            (12, " 12"),
                            (13, " 13"),
                            (14, " 14"),
                            (15, " 15"),
                            (16, " 16"),
                            (17, " 17"),
                            (18, " 18"),
                        ],
                        default=1,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HoleScore",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "score",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, " 0"),
                            (1, " 1"),
                            (2, " 2"),
                            (3, " 3"),
                            (4, " 4"),
                            (5, " 5"),
                            (6, " 6"),
                            (7, " 7"),
                            (8, " 8"),
                            (9, " 9"),
                        ],
                        default=0,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64)),
                (
                    "handicap",
                    models.DecimalField(decimal_places=1, default=20.0, max_digits=3),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True, default=None, null=True, upload_to="images"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PlayerMembership",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="dashboard.game"
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dashboard.player",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TeeTime",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tee_time", models.DateTimeField()),
                (
                    "holes_to_play",
                    models.PositiveSmallIntegerField(
                        choices=[(9, "9 Holes"), (18, "18 Holes")], default=18
                    ),
                ),
                (
                    "which_holes",
                    models.CharField(
                        choices=[("all", "All"), ("front", "Front"), ("back", "Back")],
                        default=("all", "All"),
                        max_length=5,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dashboard.golfcourse",
                    ),
                ),
                ("players", models.ManyToManyField(to="dashboard.player")),
            ],
        ),
        migrations.CreateModel(
            name="Tee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        choices=[
                            ("black", "Black"),
                            ("blue", "Blue"),
                            ("gold", "Gold"),
                            ("white", "White"),
                            ("red", "Red"),
                        ],
                        default=("blue", "Blue"),
                        max_length=5,
                        verbose_name="Tee Color",
                    ),
                ),
                (
                    "distance",
                    models.CharField(
                        max_length=3, verbose_name="Tee distance in yards"
                    ),
                ),
                (
                    "hole",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="dashboard.hole"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64)),
                (
                    "handicap",
                    models.DecimalField(decimal_places=1, default=20.0, max_digits=3),
                ),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="dashboard.game"
                    ),
                ),
                (
                    "players",
                    models.ManyToManyField(
                        through="dashboard.PlayerMembership", to="dashboard.player"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "teams",
                "ordering": ["handicap"],
            },
        ),
        migrations.AddField(
            model_name="playermembership",
            name="team",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="dashboard.team",
            ),
        ),
    ]
