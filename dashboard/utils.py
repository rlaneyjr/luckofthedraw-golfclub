import json, math, random
from dashboard import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from djmoney.money import Money

# Assuming a model named 'Item' with fields 'field1' and 'field2'
#items = Item.objects.filter(Q(field1='value1') | Q(field2='value2'))

# # How to get a random item from the database
# # first query:
# count = MyModel.objects.all().count()
#
# # second query:
# random_offset = random.randint(0,count-1)
# MyModel.objects.all()[random_offset].get()


points_map = {
    -4: 6,
    -3: 5,
    -2: 4,
    -1: 3,
    0: 2,
    1: 1,
    2: 0,
}


points_mapper = (
    {'score': -4, 'points': 6},
    {'score': -3, 'points': 5},
    {'score': -2, 'points': 4},
    {'score': -1, 'points': 3},
    {'score': 0, 'points': 2},
    {'score': 1, 'points': 1},
    {'score': 2, 'points': 0}
)


def get_score_word(strokes, par):
    if not strokes or strokes == 0:
        return _("Hole not scored")
    if strokes == 1:
        return _("Hole in One")
    elif strokes == 2:
        if par == 3:
            return _("Birdie")
        elif par == 4:
            return _("Eagle")
        elif par == 5:
            return _("Albatross")
    elif strokes == 3:
        if par == 3:
            return _("Par")
        elif par == 4:
            return _("Birdie")
        elif par == 5:
            return _("Eagle")
    elif strokes == 4:
        if par == 3:
            return _("Bogey")
        elif par == 4:
            return _("Par")
        elif par == 5:
            return _("Birdie")
    elif strokes == 5:
        if par == 4:
            return _("Bogey")
        elif par == 5:
            return _("Par")
    elif strokes == 6:
        if par == 5:
            return _("Bogey")
    return _("Double Bogey")


def round_up(x):
  frac = x - math.floor(x)
  if frac < 0.5:
    return math.floor(x)
  return math.ceil(x)


def get_avg(item_list, decimals=1):
    if not isinstance(item_list, list):
        item_list = list(item_list)
    return round(sum(item_list)/len(item_list), decimals)


def is_admin(user):
    return user.is_superuser or user.groups.filter(name="Admin").exists()


def num_players_in_skins(game):
    return models.PlayerMembership.objects.filter(game=game, skins=True).count()


def num_players_in_singles(game):
    return models.PlayerMembership.objects.filter(game=game, singles=True).count()


def get_first_course_id():
    return models.GolfCourse.objects.first().id


def set_holes_for_game(game, which_holes="all"):
    if game.course.hole_count == 18:
        if which_holes == "front":
            game.which_holes = models.WhichHolesChoices.FRONT
            game.holes_to_play = models.HolesToPlayChoices.HOLES_9
        elif which_holes == "back":
            game.which_holes = models.WhichHolesChoices.BACK
            game.holes_to_play = models.HolesToPlayChoices.HOLES_9
        else:
            game.which_holes = models.WhichHolesChoices.ALL
            game.holes_to_play = models.HolesToPlayChoices.HOLES_18
    else:
        game.which_holes = models.WhichHolesChoices.ALL
        game.holes_to_play = models.HolesToPlayChoices.HOLES_9


def set_game_type(game, game_type):
    if game_type == "best-ball":
        game.game_type = models.GameTypeChoices.BEST_BALL
    elif game_type == "stableford":
        game.game_type = models.GameTypeChoices.STABLEFORD
    elif game_type == "stroke":
        game.game_type = models.GameTypeChoices.STROKE


def get_players_not_in_game(game):
    return models.Player.objects.all().exclude(game__in=[game.id])


def get_game_player_mems(game):
    return models.PlayerMembership.objects.filter(game=game).order_by("group_id")


def get_current_players_for_game(game):
    current_players = []
    for player in game.players.all():
        player_mem = models.PlayerMembership.objects.filter(game=game, player=player).first()
        current_players.append((player, player_mem))
    return current_players


def calculate_players_handicap(players):
    if len(players) > 0:
        all_hcps = [p.handicap for p in players]
        handicap = get_avg(all_hcps)
    return handicap or 20

def get_team_hcp(team, game):
    team_members = models.PlayerMembership.objects.filter(game=game, team=team)
    all_hcps = [_t.player.handicap for _t in team_members]
    return get_avg(all_hcps)


def get_teams_for_game(game):
    return models.Team.objects.filter(game__in=[game.id])


def get_team_list_for_game(game):
    team_list = []
    for team in get_teams_for_game(game):
        team_data = {
            "id": team.id,
            "name": team.name,
            "players": [],
            "handicap": str(team.handicap),
        }
        for player in team.players.all():
            team_data["players"].append(player.name)
        team_list.append(team_data)
    return team_list


def get_groups_for_game(game):
    return models.Group.objects.filter(game__in=[game.id])


def get_group_list_for_game(game):
    group_list = []
    for group in get_groups_for_game(game):
        group_data = {
            "id": group.id,
            "name": group.name,
            "team": None,
            "players": [],
        }
        for player in group.players.all():
            player_mem = models.PlayerMembership.objects.filter(
                game=game, player=player
            ).first
            if game.use_teams and player_mem.team:
                group_data["team"] = player_mem.team
            group_data["players"].append(player)
        group_list.append(group_data)
    return group_list


# def get_par_for_course(course):
#     holes = models.Hole.objects.filter(course=course).order_by("order")
#     return sum([h.par for h in holes])


def get_holes_for_game(game):
    holes = game.course.holes
    if game.which_holes == "front":
        holes = holes.filter(order__gte=1, order__lt=10)
    elif game.which_holes == "back":
        holes = holes.filter(order__gte=10)
    return holes


def get_hole_scores_for_game(game):
    return models.HoleScore.objects.filter(player__in=[game.players]).order_by("player")


def get_hole_scores_for_player_mem(player_mem):
    return models.HoleScore.objects.filter(player=player_mem).order_by("hole")


def calculate_par_for_holes(game):
    return sum([h.par for h in get_holes_for_game(game)])


def clean_game(game):
    if game.use_groups:
        for group in get_groups_for_game(game):
            group.delete()
    if game.use_teams:
        for team in get_teams_for_game(game):
            team.delete()
    for player_mem in game.player_mems:
        player_mem.delete()


def create_holes_for_course(course):
    for hole_num in range(1, int(course.hole_count) + 1):
        hole_obj = models.Hole(
            name=f"Hole{hole_num}",
            course=course,
            order=hole_num,
            handicap=hole_num,
        )
        hole_obj.save()
    return True


def create_hole_scores_for_game(game):
    for hole in get_holes_for_game(game):
        for player in game.players.all():
            player_mem = models.PlayerMembership.objects.filter(
                player=player, game=game
            ).first()
            existing_hole_score = models.HoleScore.objects.filter(
                player=player_mem, hole=hole
            ).first()
            if existing_hole_score:
                continue
            hole_score = models.HoleScore.objects.create(player=player_mem, hole=hole)
            hole_score.save()


def calculate_teams(player_count):
    if player_count == 4:
        return 2, 2
    if player_count < 4:
        return 1, player_count
    if player_count % 4 == 0:
        return round(player_count/4), 4
    if player_count % 3 == 0:
        return round(player_count/3), 3
    if player_count % 2 == 0:
        return round(player_count/2), 2
    num_teams, num_players = calculate_teams(player_count - 1)
    if num_teams == 0:
        return 0, player_count
    return num_teams, num_players, 1


def create_players_teams(game, group=None):
    num_teams = num_players = remainder = None
    teams = []
    mem_args = {"game": game}
    if group is not None:
        players = group.players.all()
        team_name = f"{group.name}Team"
        mem_args = mem_args.update({"group": group})
    else:
        players = game.players.all()
        team_name = 'Team'
    calculated_teams = calculate_teams(players.count())
    if len(calculated_teams) == 3:
        num_teams, num_players, remainder = calculated_teams
    else:
        num_teams, num_players = calculated_teams
    for team_num in range(1, num_teams + 1):
        new_team = models.Team(name=f"{team_name}{team_num}", game=game)
        new_team.save()
        teams.append(new_team)
        for _ in range(1, num_players + 1):
            if players.count() > 0:
                _player = random.choice(players)
                mem_args.update({"player": _player})
                player_mem = models.PlayerMembership.objects.filter(**mem_args).first()
                player_mem.team = new_team
                player_mem.save()
                players = players.exclude(id=_player.id)
    if remainder and players.count() == 1:
        rem_player = players[0]
        mem_args.update({"player": rem_player})
        rem_mem = models.PlayerMembership.objects.filter(**mem_args).first()
        random_team = random.choice(teams)
        rem_mem.team = random_team
        rem_mem.save()
    for team in teams:
        team.save()


def create_teams_for_game(game):
    '''
    Not doing below. All random at the moment.
    How a Balanced Draw is calculated
    The calculation is based on the Handicap Index of those players already added to the game.
    1. The first column in the grid is filled with players with the lowest handicaps.
    2. The last column is filled with players with the highest handicaps.
    3. Any middle columns are filled with players with handicaps in the best range(s) possible.
    4. Players in each column are then randomly shuffled (column by column), to create a more random
    spread across the games.
    Pairs Competitions
    Where the Start Sheet is for a pairs competition (such as Foursomes, Four-ball, etc), HandicapMaster
    will balance the players in each team pairing (rather than across all four players in each Tee Time).
    Effectively, one player from the 50% of players with lower handicaps will be paired with one player from
    the 50% with higher handicaps.
    '''
    if game.use_groups:
        groups = get_groups_for_game(game)
        if not len(groups) == 3:
            create_groups_for_game(game)
            groups = get_groups_for_game(game)
        for group in groups:
            create_players_teams(game, group=group)
    else:
        create_players_teams(game)


def create_groups_for_game(game):
    '''
    Divide players into 3 groups based on handicap.
    Eagle Group - Top 1/3 of players with lowest handicap
    Birdie Group - Middle 1/3 of players with lowest handicap
    Par Group - Bottom 1/3 of players with lowest handicap
    '''
    count = 0
    eagle_group = models.Group.objects.filter(name=models.GroupNameChoices.EAGLE, game=game).first()
    if not eagle_group:
        eagle_group = models.Group(name=models.GroupNameChoices.EAGLE, game=game)
        eagle_group.save()
    birdie_group = models.Group.objects.filter(name=models.GroupNameChoices.BIRDIE, game=game).first()
    if not birdie_group:
        birdie_group = models.Group(name=models.GroupNameChoices.BIRDIE, game=game)
        birdie_group.save()
    par_group = models.Group.objects.filter(name=models.GroupNameChoices.PAR, game=game).first()
    if not par_group:
        par_group = models.Group(name=models.GroupNameChoices.PAR, game=game)
        par_group.save()
    players = game.players.all().order_by("-league_hcp")
    players_per_group = round(players.count()/3)
    for player in players:
        count += 1
        player_mem = models.PlayerMembership.objects.filter(game=game, player=player).first()
        if count <= players_per_group:
            eagle_group.players.add(player_mem)
        elif count <= (players_per_group*2):
            birdie_group.players.add(player_mem)
        else:
            par_group.players.add(player_mem)
    eagle_group.save()
    birdie_group.save()
    par_group.save()


def get_team_score(team):
    team_score = {
        "team_id": team.id,
        "team_name": team.name,
        "handicap": str(team.handicap),
        "players": [],
        "hole_list": [],
        "team_score": 0,
        "winner": False,
        "money": 0,
    }
    for player in team.players.all():
        team_score["players"].append(player.name)
        player_mem = models.PlayerMembership.objects.filter(
            game=team.game, player=player, team=team
        ).first()
        player_score_list = models.HoleScore.objects.filter(
            player=player_mem,
            score__gt=0,
        )
        for hole_score in player_score_list:
            hole_data = {
                "player_name": player.name,
                "hole_order": hole_score.hole.order,
                "hole_name": hole_score.hole.name,
                "hole_score": hole_score.strokes,
                "hole_par": hole_score.hole.par,
                "hole_handicap": str(hole_score.hole.handicap),
            }
            current_hole_filter = filter(
                lambda h: h["hole_order"] == hole_score.hole.order,
                team_score["hole_list"],
            )
            current_holes = list(current_hole_filter)
            if current_holes and len(current_holes) == 1:
                current_hole = current_holes[0]
                if current_hole["hole_score"] > hole_score.strokes:
                    hole_index = team_score["hole_list"].index(current_hole)
                    old_hole = team_score["hole_list"].pop(hole_index)
                    team_score["hole_list"].insert(hole_index, hole_data)
                elif current_hole["hole_score"] == hole_score.strokes:
                    hole_index = team_score["hole_list"].index(current_hole)
                    old_hole = team_score["hole_list"].pop(hole_index)
                    hole_data.update(player_name="Multiple")
                    team_score["hole_list"].insert(hole_index, hole_data)
            else:
                team_score["hole_list"].append(hole_data)
    team_score["team_score"] = sum([_h["hole_score"] for _h in team_score["hole_list"]])
    return team_score


def update_team_data_low_score(team_data, score_list, pot, percent_money=100):
    low_score = min(score_list)
    low_filter = filter(lambda t: t["team_score"] == low_score, team_data)
    team_winners = list(low_filter)
    pot_pct = percent_money/100
    money = (pot * pot_pct)/len(team_winners)
    for tw in team_winners:
        ti = team_data.index(tw)
        team = team_data.pop(ti)
        team.update({"winner": True})
        team.update({"money": str(money)})
        team_data.insert(ti, team)
        score_list.remove(tw["team_score"])
    return team_data, score_list


def score_teams(game):
    team_data = [get_team_score(t) for t in get_teams_for_game(game)]
    score_list = [td["team_score"] for td in team_data]
    if not game.payout_positions or game.payout_positions == 1:
        team_data, _ = update_team_data_low_score(team_data, score_list, game.pot)
    elif game.payout_positions == 2:
        team_data, sl = update_team_data_low_score(team_data, score_list, game.pot, 80)
        team_data, _ = update_team_data_low_score(team_data, sl, game.pot, 20)
    elif game.payout_positions == 3:
        team_data, sl = update_team_data_low_score(team_data, score_list, game.pot, 70)
        team_data, sl = update_team_data_low_score(team_data, sl, game.pot, 20)
        team_data, _ = update_team_data_low_score(team_data, sl, game.pot, 10)
    return team_data


def get_hole_list_for_game(game):
    if game.which_holes == "front":
        return list(str(i) for i in range(1, 10))
    elif game.which_holes == "back":
        return list(str(i) for i in range(10, 19))
    else:
        return list(str(i) for i in range(1, game.holes_to_play + 1))


def collect_hole_data(game, final_scores=False):
    hole_data = []
    # Always keep track of each players score
    for player in game.players.all():
        player_mem = models.PlayerMembership.objects.filter(
            game=game, player=player
        ).first()
        player_data = {
            "course_name": game.course.name,
            "player_id": player.id,
            "player_name": player.name,
            "hcp": float(player.handicap),
            "points_needed": player_mem.points_needed,
            "singles": player_mem.singles,
            "skins": player_mem.skins,
            "group_id": None,
            "group_name": None,
            "team_id": None,
            "team_name": None,
            "team_hcp": None,
            "game_hcp": None,
            "game_points": None,
            "hole_list": [],
            "player_score": 0,
            "player_points": 0,
            "par": 0,
            "money": 0,
            "singles_money": 0,
        }
        if game.use_groups and player_mem.group != None:
            player_data["group_id"] = player_mem.group.id
            player_data["group_name"] = player_mem.group.name
        if game.use_teams and player_mem.team != None:
            player_data["team_id"] = player_mem.team.id
            player_data["team_name"] = player_mem.team.name
            player_data["team_hcp"] = str(player_mem.team.handicap)
        # hole_score_list = models.HoleScore.objects.filter(player=player_mem).order_by("hole.order")
        for hole_score in player_mem.hole_scores:
            if final_scores and hole_score.strokes == 0:
                raise ValueError(f"Player {player.name} has not completed hole {hole_score.hole.name}")
            player_data["hole_list"].append(
                {
                    "hole_score_id": hole_score.id,
                    "hole_order": hole_score.hole.order,
                    "hole_name": hole_score.hole.name,
                    "hole_strokes": hole_score.strokes,
                    "hole_points": hole_score.points,
                    "hole_par": hole_score.hole.par,
                    "hole_handicap": hole_score.hole.handicap,
                    "hole_score": hole_score.score,
                }
            )
            player_data["player_score"] += hole_score.strokes
            player_data["player_points"] += hole_score.points
            player_data["par"] += hole_score.hole.par
        player_data["game_hcp"] = player_data["player_score"] - player_data["par"]
        player_data["game_points"] = player_data["player_points"] - player_data["points_needed"]
        if final_scores:
            player_mem.score_game(
                player_data["player_score"],
                player_data["game_points"],
                player_data["game_hcp"]
            )
        hole_data.append(player_data)
    return hole_data


def score_skins_for_game(game):
    skins = []
    carry_money = 0
    skin_players = models.PlayerMembership.objects.filter(
        Q(game=game) & Q(skins=True)
    )
    for hole in get_holes_for_game(game):
        hole_data = {
            "order": hole.order,
            "name": hole.name,
            "player": None,
            "money": None,
        }
        player_scores = models.HoleScore.objects.filter(
            player__in=skin_players, hole=hole
        )
        hole_money = game.skin_cost * len(skin_players)
        low_score = min([p.strokes for p in player_scores])
        low_filter = filter(lambda h: h.strokes == low_score, player_scores)
        low_scores = list(low_filter)
        if low_scores and len(low_scores) == 1:
            winner = low_scores[0].player
            money = hole_money + carry_money
            winner.skin_money += money
            winner.save()
            hole_data.update({"player": winner.name, "money": str(money)})
            carry_money = 0
        else:
            carry_money += hole_money
            hole_data.update({"player": "carry", "money": "carry"})
        skins.append(hole_data)
    skins.sort(key=lambda h: h["order"])
    return skins


def all_holes_from_hole_data(hole_data):
    all_holes = []
    for p in hole_data:
        t = {"player_name": p["player_name"]}
        for h in p["hole_list"]:
            all_holes.append(h.update(t))
    return all_holes


def filter_skins_from_all_scores(all_scores):
    skin_holes = []
    for hole in all_scores:
        skin_filter = filter(lambda s: s["skins"] == True, hole["scores"])
        hole.update({"scores": list(skin_filter)})
        skin_holes.append(hole)
    return skin_holes


def filter_skins_from_hole_data(hole_data):
    skin_holes = []
    for player in hole_data:
        if player["skins"]:
            for hole in player["hole_list"]:
                skin_hole = hole.update({"player_name": player["player_name"]})
                skin_holes.append(skin_hole)
    return skin_holes


def get_skins_hole_data(hole_data, skin_cost):
    skins = []
    carry_money = None
    skin_holes = filter_skins_from_hole_data(hole_data)
    for hole in skin_holes:
        hole_money = skin_cost * len(hole["scores"])
        low_score = min([h["strokes"] for h in hole["scores"]])
        low_filter = filter(lambda h: h["strokes"] == low_score, hole["scores"])
        low_scores = list(low_filter)
        if low_scores and len(low_scores) == 1:
            player = low_scores[0]["player"]
            if carry_money == None:
                money = hole_money
            else:
                money = hole_money + carry_money
                carry_money = None
        else:
            player = "carry"
            money = "carry"
            if carry_money == None:
                carry_money = hole_money
            else:
                carry_money += hole_money
        skins.append({"hole": hole["name"], "player": player, "money": str(money)})
    return skins


def skin_holes_from_game(game):
    skin_holes = []
    for hole in get_holes_for_game(game):
        hole_data = {
            "order": hole.order,
            "name": hole.name,
            "scores": [],
            "par": hole.par,
            "handicap": str(hole.handicap),
        }
        for player in game.players.all():
            player_mem = models.PlayerMembership.objects.filter(
                game=game, player=player
            ).first()
            if player_mem.skins:
                hole_score = models.HoleScore.objects.filter(
                    player=player_mem, hole=hole
                ).first()
                hole_data["scores"].append(
                    {
                        "player": player.name,
                        "strokes": hole_score.strokes
                    }
                )
        skin_holes.append(hole_data)
    skin_holes.sort(key=lambda s: s["order"])
    return skin_holes


def get_skins(game):
    skins = []
    carry_money = 0
    skin_holes = skin_holes_from_game(game)
    for hole in skin_holes:
        if len(hole["scores"]):
            hole_money = game.skin_cost * len(hole["scores"])
            low_score = min([h["strokes"] for h in hole["scores"]])
            low_filter = filter(lambda h: h["strokes"] == low_score, hole["scores"])
            low_scores = list(low_filter)
            if low_scores and len(low_scores) == 1:
                player = low_scores[0]["player"]
                money = hole_money + carry_money
                carry_money = 0
            else:
                player = "carry"
                money = 0
                carry_money += hole_money
            skins.append({"hole": hole["name"], "player": player, "money": str(money)})
    return skins


def tiebreaker_from_hole_hcp(winners):
    hole_hcp = 1
    while hole_hcp <= 18:
        # current_holes = []
        # for w in winners:
        #     for h in w["hole_list"]:
        #         if h["hole_handicap"] == hole_hcp:
        #             current_holes.append((w, h["hole_strokes"]))
        hole_lc = [
            (w, h["hole_strokes"]) for w in winners \
            for h in w["hole_list"] if h["hole_handicap"] == hole_hcp
        ]
        current_holes = list(hole_lc)
        low_strokes = min([s for _, s in current_holes])
        low_filter = filter(lambda s: s[1] == low_strokes, current_holes)
        low_scores = list(low_filter)
        if len(low_scores) == 1:
            winner, low_score = low_scores[0]
            return winner
        hole_hcp += 1


def get_winner(winners):
    if len(winners) == 1:
        return winners[0]
    elif len(winners) > 1:
        return tiebreaker_from_hole_hcp(winners)


def create_random_teams(game):
    teams = []
    players = list(game.players.all())
    if len(players) % 2 == 0:
        remainder = False
        num_teams = int(len(players)/2)
    else:
        remainder = True
        num_teams = int((len(players)-1)/2)
    for _num in range(1, num_teams + 1):
        new_team = models.RandomTeam(name=f"Team{_num}", game=game)
        new_team.save()
        _player_one = random.choice(players)
        new_team.players.add(_player_one)
        players = players.exclude(id=_player_one.id)
        _player_two = random.choice(players)
        new_team.players.add(_player_two)
        players = players.exclude(id=_player_two.id)
        new_team.save()
        teams.append(new_team)
    if remainder and players.count() == 1:
        rem_player = players[0]
        _lucky_team = random.choice(teams)
        _lucky_team.players.add(rem_player)
        _lucky_team.save()


def team_tiebreaker(winners):
    hole_hcp = 1
    while hole_hcp <= 18:
        current_holes = []
        for w in winners:
            current_hole = {
                "team": w,
                "strokes": 0,
            }
            for p in w.players.all():
                player_strokes = p.hole_scores.filter(hole__handicap=hole_hcp).first().strokes
                if current_hole["strokes"] == 0:
                    current_hole["strokes"] = player_strokes
                elif current_hole["strokes"] > player_strokes:
                    current_hole["strokes"] = player_strokes
            current_holes.append(current_hole)
        low_strokes = min([h["strokes"] for h in current_holes])
        low_filter = filter(lambda s: s["strokes"] == low_strokes, current_holes)
        low_scores = list(low_filter)
        if len(low_scores) == 1:
            return low_scores[0]["team"]
        hole_hcp += 1


def score_random_teams(teams, pot, percent_money=100):
    money = pot * (percent_money/100)
    high_score = max([t.points for t in teams])
    high_filter = filter(lambda t: t.points == high_score, teams)
    winners = list(high_filter)
    if len(winners) == 1:
        team_winner = winners[0]
    else:
        team_winner = team_tiebreaker(winners)
    if team_winner:
        for player in team_winner.players.all():
            player.random_money = money/team_winner.players.count()
            player.save()
        teams = teams.exclude(id=team_winner.id)
    return teams


def score_teams_random(game):
    teams = models.RandomTeam.objects.filter(game=game).order_by("points")
    if game.payout_positions == 1:
        teams = score_random_teams(teams, game.pot)
    elif game.payout_positions == 2:
        teams = score_random_teams(teams, game.pot, 80)
        teams = score_random_teams(teams, game.pot, 20)
    elif game.payout_positions == 3:
        teams = score_random_teams(teams, game.pot, 70)
        teams = score_random_teams(teams, game.pot, 20)
        teams = score_random_teams(teams, game.pot, 10)
    elif game.payout_positions == 4:
        teams = score_random_teams(teams, game.pot, 40)
        teams = score_random_teams(teams, game.pot, 30)
        teams = score_random_teams(teams, game.pot, 20)
        teams = score_random_teams(teams, game.pot, 10)


def update_player_random_money(player, money):
    player_mem = models.PlayerMembership.objects.filter(player_id=player["player_id"]).first()
    player_mem.random_money = money
    player_mem.save()


def score_hole_data_random(hole_data, pot, percent_money=100):
    money = (pot * (percent_money/100))/2
    player_one = random.choice(hole_data)
    ia = hole_data.index(player_one)
    playera = hole_data.pop(ia)
    update_player_random_money(playera, money)
    playera.update({"money": str(money)})
    hole_data.insert(ia, playera)
    player_two = random.choice(hole_data)
    ib = hole_data.index(player_two)
    playerb = hole_data.pop(ib)
    update_player_random_money(playerb, money)
    playerb.update({"money": str(money)})
    hole_data.insert(ib, playerb)


def update_player_single_money(player, money):
    player_mem = models.PlayerMembership.objects.filter(player_id=player["player_id"]).first()
    player_mem.single_money = money
    player_mem.save()


def update_hole_data_points(hole_data, points_list, pot, percent_money=100):
    high_score = max(points_list)
    high_filter = filter(lambda t: t["game_points"] == high_score, hole_data)
    winners = list(high_filter)
    money = pot * (percent_money/100)
    winner = get_winner(winners)
    i = hole_data.index(winner)
    player = hole_data.pop(i)
    update_player_single_money(player, money)
    player.update({"singles_money": str(money)})
    hole_data.insert(i, player)
    points_list.remove(winner["game_points"])
    return hole_data, points_list


def update_hole_data_score(hole_data, score_list, pot, percent_money=100):
    low_score = min(score_list)
    low_filter = filter(lambda t: t["player_score"] == low_score, hole_data)
    winners = list(low_filter)
    money = pot * (percent_money/100)
    winner = get_winner(winners)
    i = hole_data.index(winner)
    player = hole_data.pop(i)
    update_player_single_money(player, money)
    player.update({"singles_money": str(money)})
    hole_data.insert(i, player)
    score_list.remove(winner["player_score"])
    return hole_data, score_list


def score_hole_data_singles(hole_data, game):
    if game.game_type == "stableford":
        points_list = [h["game_points"] for h in hole_data if h["singles"]]
        if game.payout_positions == 1:
            hole_data, _ = update_hole_data_points(hole_data, points_list, game.single_pot)
        elif game.payout_positions == 2:
            hole_data, pl = update_hole_data_points(hole_data, points_list, game.single_pot, 80)
            hole_data, _ = update_hole_data_points(hole_data, pl, game.pot, 20)
        elif game.payout_positions == 3:
            hole_data, pl = update_hole_data_points(hole_data, points_list, game.single_pot, 70)
            hole_data, pl = update_hole_data_points(hole_data, pl, game.single_pot, 20)
            hole_data, _ = update_hole_data_points(hole_data, pl, game.single_pot, 10)
    else:
        score_list = [h["player_score"] for h in hole_data if h["singles"]]
        if payout_positions == 1:
            hole_data, _ = update_hole_data_score(hole_data, score_list, game.single_pot)
        elif payout_positions == 2:
            hole_data, sl = update_hole_data_score(hole_data, score_list, game.single_pot, 80)
            hole_data, _ = update_hole_data_score(hole_data, sl, game.single_pot, 20)
        elif payout_positions == 3:
            hole_data, sl = update_hole_data_score(hole_data, score_list, game.single_pot, 70)
            hole_data, sl = update_hole_data_score(hole_data, sl, game.single_pot, 20)
            hole_data, _ = update_hole_data_score(hole_data, sl, game.single_pot, 10)
    return hole_data


def score_hole_data(hole_data, game):
    if game.game_type == "stableford":
        points_list = [h["game_points"] for h in hole_data]
        if game.payout_positions == 1:
            hole_data, _ = score_hole_data_points(hole_data, points_list, game.pot)
        elif game.payout_positions == 2:
            hole_data, pl = score_hole_data_points(hole_data, points_list, game.pot, 80)
            hole_data, _ = score_hole_data_points(hole_data, pl, game.pot, 20)
        elif game.payout_positions == 3:
            hole_data, pl = score_hole_data_points(hole_data, points_list, game.pot, 70)
            hole_data, pl = score_hole_data_points(hole_data, pl, game.pot, 20)
            hole_data, _ = score_hole_data_points(hole_data, pl, game.pot, 10)
    else:
        score_list = [h["player_score"] for h in hole_data]
        if payout_positions == 1:
            hole_data, _ = score_hole_data_score(hole_data, score_list, game.pot)
        elif payout_positions == 2:
            hole_data, sl = score_hole_data_score(hole_data, score_list, game.pot, 80)
            hole_data, _ = score_hole_data_score(hole_data, sl, game.pot, 20)
        elif payout_positions == 3:
            hole_data, sl = score_hole_data_score(hole_data, score_list, game.pot, 70)
            hole_data, sl = score_hole_data_score(hole_data, sl, game.pot, 20)
            hole_data, _ = score_hole_data_score(hole_data, sl, game.pot, 10)
    return hole_data


def get_player_league_items(player, item):
    league_mems = models.PlayerMembership.objects.filter(
        player=player, game__league_game=True
    )
    return list(league_mems.values_list(item, flat=True))


def get_player_item_league_avg(player, item, required_length: int=None):
    item_list = get_player_league_items(player, item)
    if isinstance(required_length, int) and len(item_list) < required_length:
        return None
    return get_avg(item_list, 1)


def calculate_player_league_hcp(player, hcp=None):
    league_hcp = 20
    rl = 3 if hcp is None else 2
    league_hcps = get_player_item_league_avg(player, "game_handicap", rl)
    if league_hcps:
        if hcp is not None:
            league_hcps.append(hcp)
        league_hcp = get_avg(league_hcps, 1)
    return league_hcp


def update_player_hcp(player, hcp=None):
    new_hcp = calculate_player_league_hcp(player, hcp)
    if new_hcp and new_hcp != player.handicap:
        player.handicap = new_hcp
        player.save()
    elif hcp:
        player.handicap = hcp
        player.save()


def update_player_hcp_hole_data(hole_data):
    for pd in hole_data:
        player = models.Player.objects.filter(pk=pd["player_id"]).first()
        update_player_hcp(player, pd["game_hcp"])


def revert_player_hcp(player_mem):
    current_hcps = models.PlayerMembership.objects.filter(
        player=player_mem.player,
        game_handicap__isnull=False,
        game__league_game=True
    ).exclude(id__in=[player_mem.id]).values_list("game_handicap", flat=True)
    hcps = list(current_hcps)
    update_player_hcp(get_avg(hcps, 1))


def score_game(game):
    # hole_list = get_hole_list_for_game(game)
    # all_scores = collect_skin_data(game)
    # for hole in all_scores:
    #     for score in hole['scores']:
    #         if score['strokes'] == 0:
    #             raise ValueError(f"Player {score['player']} has not completed hole {hole['name']}")
    hole_data = collect_hole_data(game, final_scores=True)
    game_score = {
        "scores": hole_data,
        "skins": False,
        "team_scores": False,
    }
    if game.single_cost != 0:
        game_score.update(
            {"scores": score_hole_data_singles(hole_data, game)}
        )
    if game.skin_cost != 0:
        game_score.update({"skins": score_skins_for_game(game)})
    if game.use_teams:
        game_score.update({"team_scores": score_teams(game)})
    if game.league_game:
        update_player_hcp_hole_data(hole_data)
        create_random_teams(game)
        score_teams_random(game)
    return game_score


def get_player_scores_for_course(player, course):
    scores = []
    for game in models.Game.objects.filter(course=course, league_game=True):
        if player in game.players.all():
            player_mem = models.PlayerMembership.objects.filter(
                game=game, player=player
            ).first()
            scores.append(player_mem.game_score)
    return scores


def get_player_league_standings(player, course):
    scores = get_player_scores_for_course(player, course)
    if not len(scores):
        avg = f"HCP:{player.handicap}"
        points = course.points - round_up(player.handicap)
    elif len(scores) > 1:
        avg = round_up(sum(scores)/len(scores))
        points = course.points - (avg - course.par)
    return avg, points


def get_league_standings():
    league_standings = []
    for player in models.Player.objects.all():
        points = 36 - round_up(player.handicap)
        player_standing = {
            "id": player.id,
            "name": player.name,
            "hcp": player.handicap,
            "points": points
        }
        league_standings.append(player_standing)
    league_standings.sort(key=lambda p: p["hcp"])
    rank = 0
    for person in league_standings:
        rank += 1
        person.update({"rank": rank})
    return league_standings


def get_ranked_players():
    player_standings = []
    for player in models.Player.objects.all():
        _player = {
            "player": player,
            "hcp": player.handicap,
        }
        player_standings.append(_player)
    player_standings.sort(key=lambda p: p["hcp"])
    rank = 0
    player_list = []
    for person in player_standings:
        rank += 1
        player_list.append((rank, person["player"]))
    return player_list
