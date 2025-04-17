from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator
from djmoney.money import Money
from dashboard import utils

User = get_user_model()


def get_ttcc_course():
    return GolfCourse.objects.get(initials="TTCC").id


class GameTypeChoices(models.TextChoices):
    BEST_BALL = "best-ball", _("Best Ball")
    STROKE = "stroke", _("Stroke")
    STABLEFORD = "stableford", _("Stableford")


class GameStatusChoices(models.TextChoices):
    SETUP = "setup", _("Setup")
    ACTIVE = "active", _("Active")
    COMPLETED = "completed", _("Completed")


class PayoutChoices(models.IntegerChoices):
    _1 = 1
    _2 = 2
    _3 = 3


class GroupNameChoices(models.TextChoices):
    EAGLE = "Eagle", _("Eagle")
    BIRDIE = "Birdie", _("Birdie")
    PAR = "Par", _("Par")


class HoleNameChoices(models.TextChoices):
    HOLE_1 = "Hole1", _("Hole 1")
    HOLE_2 = "Hole2", _("Hole 2")
    HOLE_3 = "Hole3", _("Hole 3")
    HOLE_4 = "Hole4", _("Hole 4")
    HOLE_5 = "Hole5", _("Hole 5")
    HOLE_6 = "Hole6", _("Hole 6")
    HOLE_7 = "Hole7", _("Hole 7")
    HOLE_8 = "Hole8", _("Hole 8")
    HOLE_9 = "Hole9", _("Hole 9")
    HOLE_10 = "Hole10", _("Hole 10")
    HOLE_11 = "Hole11", _("Hole 11")
    HOLE_12 = "Hole12", _("Hole 12")
    HOLE_13 = "Hole13", _("Hole 13")
    HOLE_14 = "Hole14", _("Hole 14")
    HOLE_15 = "Hole15", _("Hole 15")
    HOLE_16 = "Hole16", _("Hole 16")
    HOLE_17 = "Hole17", _("Hole 17")
    HOLE_18 = "Hole18", _("Hole 18")


class ParChoices(models.IntegerChoices):
    PAR_3 = 3, _("Par 3")
    PAR_4 = 4, _("Par 4")
    PAR_5 = 5, _("Par 5")


class OrderChoices(models.IntegerChoices):
    _1 = 1
    _2 = 2
    _3 = 3
    _4 = 4
    _5 = 5
    _6 = 6
    _7 = 7
    _8 = 8
    _9 = 9
    _10 = 10
    _11 = 11
    _12 = 12
    _13 = 13
    _14 = 14
    _15 = 15
    _16 = 16
    _17 = 17
    _18 = 18


class TeeColorChoices(models.TextChoices):
    BLACK = "black", _("Black")
    BLUE = "blue", _("Blue")
    GOLD = "gold", _("Gold")
    WHITE = "white", _("White")
    GREEN = "green", _("Green")
    RED = "red", _("Red")
    ORANGE = "orange", _("Orange")


class HolesToPlayChoices(models.IntegerChoices):
    HOLES_9 = 9, _("9 Holes")
    HOLES_18 = 18, _("18 Holes")


class WhichHolesChoices(models.TextChoices):
    ALL = "all", _("All")
    FRONT = "front", _("Front 9")
    BACK = "back", _("Back 9")


class StrokeChoices(models.IntegerChoices):
    _0 = 0
    _1 = 1
    _2 = 2
    _3 = 3
    _4 = 4
    _5 = 5
    _6 = 6
    _7 = 7
    _8 = 8
    _9 = 9


class GolfCourse(models.Model):
    name = models.CharField(max_length=128)
    initials = models.CharField(
        verbose_name="Course Initials",
        max_length=5,
        default="GC"
    )
    hole_count = models.PositiveSmallIntegerField(
        choices=HolesToPlayChoices.choices,
        default=HolesToPlayChoices.HOLES_18
    )
    tee_time_link = models.URLField(blank=True)
    website_link = models.URLField(blank=True)
    city = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=64, blank=True)
    zip_code = models.CharField(max_length=128, blank=True)
    card = models.ImageField(
        upload_to="images",
        default=None,
        blank=True,
        null=True
    )
    overview = models.ImageField(
        upload_to="images",
        default=None,
        blank=True,
        null=True
    )
    par = models.PositiveSmallIntegerField(
        default=None,
        blank=True,
        null=True
    )
    points = models.PositiveSmallIntegerField(
        default=None,
        blank=True,
        null=True
    )

    class Meta:
        unique_together = ["name", "city", "state"]
        ordering = ["state", "city"]

    def __str__(self):
        return f"{self.initials}"

    def __repr__(self):
        return f"Course[{self.initials}]"

    def __update_par_points(self):
        holes = Hole.objects.filter(course=self)
        if holes.count() == self.hole_count:
            self.par = sum([h.par for h in holes])
            self.points = utils.round_up(self.par/2)

    def save(self, *args, **kwargs):
        self.__update_par_points()
        super().save(*args, **kwargs)


class Hole(models.Model):
    name = models.CharField(
        max_length=7,
        choices=HoleNameChoices.choices,
        default=HoleNameChoices.HOLE_1
    )
    nickname = models.CharField(max_length=64, blank=True)
    par = models.PositiveSmallIntegerField(
        choices=ParChoices.choices,
        default=ParChoices.PAR_4
    )
    course = models.ForeignKey(GolfCourse, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(
        choices=OrderChoices.choices,
        default=OrderChoices._1
    )
    handicap = models.PositiveSmallIntegerField(
        choices=OrderChoices.choices,
        default=OrderChoices._1
    )

    def __str__(self):
        return f"{self.course}-{self.name}"

    def __repr__(self):
        return f"Hole[{self.course}:{self.name}]"

    class Meta:
        unique_together = ["name", "course", "order", "handicap"]
        ordering = ["course", "order"]


class Tee(models.Model):
    hole = models.ForeignKey(Hole, on_delete=models.CASCADE)
    color = models.CharField(
        verbose_name="Tee Color",
        max_length=6,
        choices=TeeColorChoices.choices,
        default=TeeColorChoices.BLACK,
    )
    distance = models.CharField(
        verbose_name="Tee distance in yards",
        max_length=3
    )

    def __str__(self):
        return f"{self.hole}-{self.color}"

    def __repr__(self):
        return f"Tee[{self.hole}:{self.color}]"

    class Meta:
        unique_together = ["hole", "color"]
        ordering = ["hole", "-distance"]


class Game(models.Model):
    """
    singles = per group
    blind draw = per game overall
    skins = per game overall
    """
    course = models.ForeignKey(
        GolfCourse,
        on_delete=models.PROTECT,
        default=get_ttcc_course,
    )
    game_type = models.CharField(
        max_length=32,
        choices=GameTypeChoices.choices,
        default=GameTypeChoices.STABLEFORD,
    )
    date_played = models.DateTimeField(default=timezone.now)
    holes_to_play = models.PositiveSmallIntegerField(
        choices=HolesToPlayChoices.choices,
        default=HolesToPlayChoices.HOLES_18
    )
    which_holes = models.CharField(
        max_length=5,
        choices=WhichHolesChoices.choices,
        default=WhichHolesChoices.ALL,
    )
    status = models.CharField(
        max_length=64,
        choices=GameStatusChoices.choices,
        default=GameStatusChoices.SETUP,
    )
    players = models.ManyToManyField(
        "Player",
        through="PlayerMembership",
        through_fields=("game", "player")
    )
    buy_in = MoneyField(
        name="buy_in",
        verbose_name="Per-player random draw buy-in",
        max_digits=3,
        decimal_places=0,
        default=10,
        default_currency="USD",
        validators=[
            MinMoneyValidator({"USD": 0}),
            MaxMoneyValidator({"USD": 100}),
        ],
    )
    skin_cost = MoneyField(
        name="skin_cost",
        verbose_name="Per-hole skin buy-in",
        max_digits=3,
        decimal_places=0,
        default=1,
        default_currency="USD",
        validators=[
            MinMoneyValidator({"USD": 0}),
            MaxMoneyValidator({"USD": 100}),
        ],
    )
    single_cost = MoneyField(
        name="single_cost",
        verbose_name="Per-Player singles buy-in",
        max_digits=3,
        decimal_places=0,
        default=5,
        default_currency="USD",
        validators=[
            MinMoneyValidator({"USD": 0}),
            MaxMoneyValidator({"USD": 100}),
        ],
    )
    score = models.JSONField(blank=True, null=True)
    use_groups = models.BooleanField(default=True)
    use_teams = models.BooleanField(default=False)
    league_game = models.BooleanField(default=True)
    payout_positions = models.PositiveSmallIntegerField(
        choices=PayoutChoices.choices,
        default=PayoutChoices._1,
    )

    @property
    def par(self):
        if self.holes_to_play == HolesToPlayChoices.HOLES_9:
            return utils.get_par_for_game(self)
        else:
            return self.course.par

    @property
    def player_mems(self):
        return utils.get_game_player_mems(self)

    @property
    def pot(self):
        return self.buy_in * self.players.count()

    @property
    def points(self):
        return self.course.points

    @property
    def skin_count(self):
        return utils.num_players_in_skins(self)

    @property
    def single_count(self):
        return utils.num_players_in_singles(self)

    @property
    def skin_pot(self):
        return self.skin_cost * self.holes_to_play * self.skin_count

    @property
    def single_pot(self):
        return self.single_cost * self.single_count

    def __str__(self):
        if self.status == GameStatusChoices.COMPLETED:
            return f"{self.course}-{self.date_played.date()}"
        return f"{self.course}-{self.status}"

    def __repr__(self):
        return f"Game[{str(self).replace('-', ':')}]"

    def set_holes(self, which_holes="all"):
        if self.course.hole_count == 18:
            if which_holes == "front":
                self.which_holes = WhichHolesChoices.FRONT
                self.holes_to_play = HolesToPlayChoices.HOLES_9
            elif which_holes == "back":
                self.which_holes = WhichHolesChoices.BACK
                self.holes_to_play = HolesToPlayChoices.HOLES_9
            else:
                self.which_holes = WhichHolesChoices.ALL
                self.holes_to_play = HolesToPlayChoices.HOLES_18
        else:
            self.which_holes = WhichHolesChoices.ALL
            self.holes_to_play = HolesToPlayChoices.HOLES_9
        self.save()

    def set_type(self, game_type):
        if game_type == "best-ball":
            self.game_type = GameTypeChoices.BEST_BALL
        elif game_type == "stableford":
            self.game_type = GameTypeChoices.STABLEFORD
        elif game_type == "stroke":
            self.game_type = GameTypeChoices.STROKE
        self.save()

    def start(self, **kwargs):
        for key, value in kwargs.items():
            if key == "which_holes":
                self.set_holes(value)
            elif "type" in key:
                self.set_type(value)
            elif hasattr(self, key):
                setattr(self, key, value)
                self.save()
        utils.create_hole_scores_for_game(self)
        if self.use_teams or all([self.use_groups, self.use_teams]):
            utils.create_teams_for_game(self)
        elif self.use_groups:
            utils.create_groups_for_game(self)
        self.status = GameStatusChoices.ACTIVE
        self.save()

    def stop(self):
        if self.status != GameStatusChoices.COMPLETED:
            self.score = utils.score_game(self)
            self.status = GameStatusChoices.COMPLETED
            self.save()

    def reset(self):
        if self.status != GameStatusChoices.COMPLETED:
            utils.clean_game(self)
            self.score = None
            self.status = GameStatusChoices.SETUP
            self.save()

    def clean(self):
        num_holes = self.course.hole_count - self.holes_to_play
        if num_holes == 9 and self.which_holes == WhichHolesChoices.ALL:
            raise ValidationError("Please choose front or back")

    # def delete(self, *args, **kwargs):
    #     utils.clean_game(self)
    #     super().delete(*args, **kwargs)

    class Meta:
        ordering = ["date_played", "status"]
        verbose_name_plural = "games"
        get_latest_by = "date_played"
        unique_together = ["course", "date_played"]


class Player(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(
        max_length=254,
        default=None,
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=12,
        default=None,
        blank=True,
        null=True
    )
    handicap = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=20.0
    )
    photo = models.ImageField(
        upload_to="images",
        default=None,
        blank=True,
        null=True
    )
    user_account = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True
    )
    added_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="added_by"
    )

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def league_hcp(self):
        return utils.calculate_player_league_hcp(self) or self.handicap

    @property
    def league_points(self):
        return utils.get_player_item_league_avg(self, 'game_points')

    @property
    def league_score(self):
        return utils.get_player_item_league_avg(self, 'game_score')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Player[{self.name}]"

    def update_handicap(self, hcp=None):
        if hcp is not None:
            self.handicap = hcp
            self.save()
        elif self.handicap != self.league_hcp:
            self.handicap = self.league_hcp
            self.save()

    # def save(self, *args, **kwargs):
    #     if self.handicap != self.league_hcp:
    #         self.handicap = self.league_hcp
    #     super().save(*args, **kwargs)

    class Meta:
        unique_together = ["first_name", "last_name"]
        ordering = ["handicap", "last_name", "first_name"]
        verbose_name_plural = "players"


class Team(models.Model):
    name = models.CharField(max_length=32)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    players = models.ManyToManyField(
        "Player",
        through="PlayerMembership",
        through_fields=("team", "player")
    )
    handicap = models.DecimalField(
        max_digits=3, decimal_places=1, default=20.0
    )

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"Team[{self.name}]"

    def save(self, *args, **kwargs):
        if len(self.players.all()) > 0:
            all_hcps = [p.handicap for p in self.players.all()]
            self.handicap = utils.get_avg(all_hcps)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["game", "name"]
        verbose_name_plural = "teams"
        unique_together = ["name", "game"]


class Group(models.Model):
    name = models.CharField(
        max_length=32,
        choices=GroupNameChoices.choices,
        default=GroupNameChoices.PAR,
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    players = models.ManyToManyField(
        "Player",
        through="PlayerMembership",
        through_fields=("group", "player")
    )

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"Group[{self.name}]"

    class Meta:
        ordering = ["game", "name"]
        verbose_name_plural = "groups"
        unique_together = ["name", "game"]


class PlayerMembership(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_DEFAULT,
        default=None,
        blank=True,
        null=True
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_DEFAULT,
        default=None,
        blank=True,
        null=True
    )
    skins = models.BooleanField(default=False)
    singles = models.BooleanField(default=False)
    game_handicap = models.SmallIntegerField(
        default=None,
        blank=True,
        null=True
    )
    game_score = models.SmallIntegerField(
        default=None,
        blank=True,
        null=True
    )
    game_points = models.SmallIntegerField(
        default=None,
        blank=True,
        null=True
    )

    @property
    def is_official(self):
        if all([self.game_handicap, self.game_points, self.game_score]) and \
                (self.game is None or (self.game.league_game and \
                self.game.status == GameStatusChoices.COMPLETED)):
            return True
        return False

    @property
    def name(self):
        return self.player.name

    @property
    def hole_scores(self):
        return HoleScore.objects.filter(player=self).order_by("hole")

    @property
    def points_needed(self):
        return self.game.points - utils.round_up(self.player.league_hcp)

    @property
    def league_hcp(self):
        return self.player.league_hcp

    @property
    def league_points(self):
        return self.player.league_points

    @property
    def league_score(self):
        return self.player.league_score

    def __str__(self):
        name = f"{self.name}"
        if self.game is not None:
            name = f"{name}-{self.game}"
        if self.group is not None:
            name = f"{name}-{self.group}"
        if self.team is not None:
            name = f"{name}-{self.team}"
        return name

    def __repr__(self):
        return f"PlayerMembership[{str(self).replace('-', ':')}]"

    def score_game(self, game_score, game_points, game_hcp):
        if all([game_score, game_points, game_hcp]):
            self.game_score = game_score
            self.game_points = game_points
            self.game_handicap = game_hcp
            self.save()

    def delete(self, *args, **kwargs):
        if self.is_official:
            utils.revert_player_hcp(self.player, self.game_handicap)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.is_official:
            utils.update_player_hcp(self.player, self.game_handicap)
        super().save(*args, **kwargs)

    class Meta:
        order_with_respect_to = "player"


class HoleScore(models.Model):
    player = models.ForeignKey(PlayerMembership, on_delete=models.CASCADE)
    hole = models.ForeignKey(Hole, on_delete=models.CASCADE)
    strokes = models.PositiveSmallIntegerField(
        choices=StrokeChoices.choices,
        default=StrokeChoices._0
    )

    @property
    def is_scored(self):
        if self.strokes == StrokeChoices._0:
            return False
        return True

    @property
    def max_strokes(self):
        return self.hole.par + max(utils.points_map.keys())

    @property
    def score(self):
        if self.is_scored:
            return self.strokes - self.hole.par
        else:
            return 0

    @property
    def points(self):
        if self.is_scored:
            return utils.points_map.get(self.score, 0)
        else:
            return 0

    @property
    def score_name(self):
        return utils.get_score_word(self.strokes, self.hole.par)

    def __str__(self):
        return f"{self.player}-{self.hole}"

    def __str__(self):
        return f"HoleScore[{self.player}:{self.hole}]"

    def score_hole(self, strokes: int=None):
        if isinstance(strokes, int) and self.strokes != strokes:
            if strokes > self.max_strokes:
                self.strokes = self.max_strokes
            else:
                self.strokes = strokes
            self.save()

    def reset_score(self):
        if self.is_scored:
            self.strokes = StrokeChoices._0
            self.save()

    class Meta:
        ordering = ["player", "hole", "-strokes"]
        verbose_name_plural = "scores"
        unique_together = ["player", "hole"]


class TeeTime(models.Model):
    course = models.ForeignKey(GolfCourse, on_delete=models.CASCADE)
    tee_time = models.DateTimeField()
    players = models.ManyToManyField("Player")
    holes_to_play = models.PositiveSmallIntegerField(
        choices=HolesToPlayChoices.choices,
        default=HolesToPlayChoices.HOLES_18
    )
    which_holes = models.CharField(
        max_length=5,
        choices=WhichHolesChoices.choices,
        default=WhichHolesChoices.ALL,
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.course}-{self.tee_time.date()}"

    def __repr__(self):
        return f"TeeTime[{self.course}:{self.tee_time.date()}]"

    def clean(self):
        num_holes = self.course.hole_count - self.holes_to_play
        if num_holes == 9 and self.which_holes == WhichHolesChoices.ALL:
            raise ValidationError("Please choose front or back")

    class Meta:
        ordering = ["tee_time"]
        verbose_name_plural = "tee_times"

