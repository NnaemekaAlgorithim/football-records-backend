from uuid import uuid4
from django.db import models
from django.forms import ValidationError
from .base_model import BaseModel

class PlayerStats(BaseModel):
    """Represents player statistics for a MySQL database.
    
    Attributes:
        stat_id (UUIDField): The statistics ID (primary key).
        CustomUser (ForeignKey): The ID of the user (foreign key).
        current_team (CharField): The name of current team.
        previous_team (CharField): The name of the player's previous team.
        joined_team_at (CharField): When the player joined the team.
        left_team_at (CharField): When the player left the team.
        season_played (CharField): The season the statistics were recorded.
        match_half_played (CharField): The match half played.
        start_match (BooleanField): Whether the player started the match.
        sub_in_at (CharField): The time the player was substituted in.
        sub_out_at (CharField): The time the player was substituted out.
        opposing_team (CharField): The opposing team.
        match_type (CharField): The type of match.
        control_success (IntegerField): Number of successful controls.
        control_fail (IntegerField): Number of failed controls.
        short_pass_success (IntegerField): Number of successful short passes.
        short_pass_fail (IntegerField): Number of failed short passes.
        duel_success (IntegerField): Number of successful duels.
        duel_fail (IntegerField): Number of failed duels.
        long_pass_success (IntegerField): Number of successful long passes.
        long_pass_fail (IntegerField): Number of failed long passes.
        dribble_success (IntegerField): Number of successful dribbles.
        dribble_fail (IntegerField): Number of failed dribbles.
        cross_success (IntegerField): Number of successful crosses.
        cross_fail (IntegerField): Number of failed crosses.
        shoot_success (IntegerField): Number of successful shots.
        shoot_fail (IntegerField): Number of failed shots.
        interception_success (IntegerField): Number of successful interceptions.
        interception_fail (IntegerField): Number of failed interceptions.
        one_touch_pass_success (IntegerField): Number of successful one-touch passes.
        one_touch_pass_fail (IntegerField): Number of failed one-touch passes.
        call_of_ball_success (IntegerField): Number of successful calls of the ball.
        call_of_ball_fail (IntegerField): Number of failed calls of the ball.
        tackle_success (IntegerField): Number of successful tackles.
        tackle_fail (IntegerField): Number of failed tackles.
        clearance_success (IntegerField): Number of successful clearances.
        clearance_fail (IntegerField): Number of failed clearances.
        fouled_on (IntegerField): Number of times fouled on.
        foul_commited (IntegerField): Number of fouls committed.
        corner_success (IntegerField): Number of successful corners.
        corner_fail (IntegerField): Number of failed corners.
        free_kick_success (IntegerField): Number of successful free kicks.
        free_kick_fail (IntegerField): Number of failed free kicks.
        penalty_kick_success (IntegerField): Number of successful penalty kicks.
        penalty_kick_fail (IntegerField): Number of failed penalty kicks.
        yellow_card (IntegerField): Number of yellow cards received.
        red_card (IntegerField): Number of red cards received.
        goal_save (IntegerField): Number of goals saved.
        goal_conceded (IntegerField): Number of goals conceded.
        penalty_save (IntegerField): Number of penalties saved.
        penalty_conceded (IntegerField): Number of penalties conceded.
        offside (IntegerField): Number of offsides.
        goal_scored (IntegerField): Number of goals scored.
        assists (IntegerField): Number of assists.
        throw_in_success (IntegerField): Number of successful throw-ins.
        throw_in_fail (IntegerField): Number of failed throw-ins.
    """
    stat_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    player = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='player_stats', limit_choices_to={'is_player': True})
    current_team = models.CharField(max_length=128)
    previous_team = models.CharField(max_length=128, null=True, blank=True)
    joined_team_at = models.CharField(max_length=128, null=True, blank=True)
    left_team_at = models.CharField(max_length=128, null=True, blank=True)
    season_played = models.CharField(max_length=128, null=True, blank=True)
    match_half_played = models.CharField(max_length=128, null=True, blank=True)
    start_match = models.BooleanField(default=False)
    sub_in_at = models.CharField(max_length=128, null=True, blank=True)
    sub_out_at = models.CharField(max_length=128, null=True, blank=True)
    opposing_team = models.CharField(max_length=128)
    match_type = models.CharField(max_length=128)
    control_success = models.IntegerField(default=0)
    control_fail = models.IntegerField(default=0)
    short_pass_success = models.IntegerField(default=0)
    short_pass_fail = models.IntegerField(default=0)
    duel_success = models.IntegerField(default=0)
    duel_fail = models.IntegerField(default=0)
    long_pass_success = models.IntegerField(default=0)
    long_pass_fail = models.IntegerField(default=0)
    dribble_success = models.IntegerField(default=0)
    dribble_fail = models.IntegerField(default=0)
    cross_success = models.IntegerField(default=0)
    cross_fail = models.IntegerField(default=0)
    shoot_success = models.IntegerField(default=0)
    shoot_fail = models.IntegerField(default=0)
    interception_success = models.IntegerField(default=0)
    interception_fail = models.IntegerField(default=0)
    one_touch_pass_success = models.IntegerField(default=0)
    one_touch_pass_fail = models.IntegerField(default=0)
    call_of_ball_success = models.IntegerField(default=0)
    call_of_ball_fail = models.IntegerField(default=0)
    tackle_success = models.IntegerField(default=0)
    tackle_fail = models.IntegerField(default=0)
    clearance_success = models.IntegerField(default=0)
    clearance_fail = models.IntegerField(default=0)
    fouled_on = models.IntegerField(default=0)
    foul_commited = models.IntegerField(default=0)
    corner_success = models.IntegerField(default=0)
    corner_fail = models.IntegerField(default=0)
    free_kick_success = models.IntegerField(default=0)
    free_kick_fail = models.IntegerField(default=0)
    penalty_kick_success = models.IntegerField(default=0)
    penalty_kick_fail = models.IntegerField(default=0)
    yellow_card = models.IntegerField(default=0)
    red_card = models.IntegerField(default=0)
    goal_save = models.IntegerField(default=0)
    goal_conceded = models.IntegerField(default=0)
    penalty_save = models.IntegerField(default=0)
    penalty_conceded = models.IntegerField(default=0)
    offside = models.IntegerField(default=0)
    goal_scored = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    throw_in_success = models.IntegerField(default=0)
    throw_in_fail = models.IntegerField(default=0)

    def __str__(self):
        return f"Stats for {self.player} in {self.season_played}"
    
    def save(self, *args, **kwargs):
        if not self.player.is_player:
            raise ValidationError("The user must be a player.")
        super().save(*args, **kwargs)
