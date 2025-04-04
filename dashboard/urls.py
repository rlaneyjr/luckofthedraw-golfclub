from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns =  [
    path("", views.dashboard, name="dashboard"),
    path("profile/", views.my_profile, name="profile"),
    path(
        "download-scorecard/<int:game_pk>/",
        views.download_scorecard,
        name="download-scorecard",
    ),
    path("location-test/", views.location_test, name="location-test"),
    path("no-permission/", views.no_permission, name="no_permission"),
    path("courses/", views.course_list, name="courses"),
    path("courses/add/", views.create_course, name="create_course"),
    path("courses/<int:pk>/", views.course_detail, name="course_detail"),
    path("courses/<int:pk>/edit/", views.edit_course, name="edit_course"),
    path("courses/<int:pk>/add/", views.create_hole, name="create_hole"),
    path("holes/<int:pk>/", views.hole_detail, name="hole_detail"),
    path("holes/<int:pk>/edit/", views.edit_hole, name="edit_hole"),
    path("tees/<int:hole_pk>/add/", views.create_tee, name="create_tee"),
    path("tees/<int:hole_pk>/edit/", views.edit_tee, name="edit_tee"),
    path("games/", views.game_list, name="games"),
    path("games/<int:pk>/", views.game_detail, name="game_detail"),
    path("games/<int:pk>/edit", views.edit_game, name="edit_game"),
    path("games/<int:pk>/score", views.game_score, name="game_score"),
    path("games/<int:pk>/score_details", views.game_score_detail, name="game_score_detail"),
    path("games/add/", views.create_game, name="create_game"),
    path("games/mine/", views.view_my_games, name="my-game-list"),
    path("players/", views.player_list, name="players"),
    path("players/<int:pk>/", views.player_detail, name="player_detail"),
    path("players/add/", views.create_player, name="create_player"),
    path("players/<int:pk>/edit/", views.edit_player, name="edit_player"),
    path("holescores/<int:pk>/", views.hole_score_detail, name="hole_score_detail"),
    path("holescores/<int:pk>/edit/", views.edit_hole_score, name="edit_hole_score"),
    path("tee-times/", views.tee_time_list, name="tee_times"),
    path("tee-times/add/", views.create_tee_time, name="create_tee_time"),
    path("tee-times/<int:pk>/", views.tee_time_detail, name="tee_time_detail"),
    # ajax
    path("ajax/manage-game/", views.ajax_manage_game, name="ajax_manage_game"),
    path("ajax/delete-tee/", views.ajax_delete_tee, name="ajax_delete_tee"),
    path(
        "ajax/add-player-to-game/",
        views.ajax_manage_players_for_game,
        name="ajax_manage_players_for_game",
    ),
    path(
        "ajax/record-score-for-hole/",
        views.ajax_record_score_for_hole,
        name="ajax_record_score_for_hole",
    ),
    path(
        "ajax/edit-hole-score/",
        views.ajax_edit_hole_score,
        name="ajax_edit_hole_score",
    ),
    path(
        "ajax/manage_tee_time/",
        views.ajax_manage_tee_time,
        name="ajax_manage_tee_time",
    ),
    path(
        "ajax/delete_hole_score/",
        views.ajax_delete_hole_score,
        name="ajax_delete_hole_score",
    ),
]
