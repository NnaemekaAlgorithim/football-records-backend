from uuid import uuid4
from django.db import models
from django.conf import settings
from .base_model import BaseModel

class TeamStats(BaseModel):
    """Represents team statistics for a MySQL database.
    
    Attributes:
        team_stat_id (UUIDField): The statistics ID (primary key).
        season (ForeignKey): The season the statistics were recorded.
        league (ForeignKey): The league in which the match was played.
        team_name (ForeignKey): The name of the team (foreign key).
        team_logo (ForeignKey): The logo of the team (foreign key).
        opposing_team_name (CharField): The name of the opposing team.
        match_outcome (CharField): Indicates the outcome of the match.
        match_goals (IntegerField): Number of goals scored in the match.
        match_concided_goals (IntegerField): Number of goals conceded in the match.
        match_goal_scored_time (JSONField): List of times when goals were scored during the match.
        match_goal_concided_time (JSONField): List of times when goals were conceded during the match.
        match_possession (FloatField): Indicates the possession for the match.
        total_number_of_goals (IntegerField): Total number of goals scored by the team.
        total_number_of_wins (IntegerField): Total number of wins by the team.
        total_number_of_loses (IntegerField): Total number of losses by the team.
        total_number_of_draws (IntegerField): Total number of draws by the team.
        total_number_of_matches_played (IntegerField): Total number of matches played by the team.
        total_number_of_passes (IntegerField): Total number of passes made by the team.
        players (ManyToManyField): List of all players in the team at the time of the match.
    """

    WIN = 'win'
    DRAW = 'draw'
    LOSS = 'loss'

    MATCH_OUTCOME_CHOICES = [
        (WIN, 'Win'),
        (DRAW, 'Draw'),
        (LOSS, 'Loss'),
    ]

    team_stat_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    season = models.ForeignKey('Season', on_delete=models.CASCADE, related_name='team_stats')
    league = models.ForeignKey('League', on_delete=models.CASCADE, related_name='team_stats', null=True)
    team_name = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='team_stats')
    team_logo = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='team_logo_stats')
    opposing_team_name = models.CharField(null=True, max_length=128)
    match_outcome = models.CharField(max_length=4, choices=MATCH_OUTCOME_CHOICES)
    match_goals = models.IntegerField(default=0)
    match_concided_goals = models.IntegerField(default=0)
    match_goal_scored_time = models.JSONField(default=list, help_text="List of times when goals were scored during the match")
    match_goal_concided_time = models.JSONField(default=list, help_text="List of times when goals were conceded during the match")
    match_possession = models.FloatField(null=True, blank=True)
    players = models.ManyToManyField('Player', related_name='team_stats')

    def __str__(self):
        return f"Stats for {self.team_name.team_name} in {self.season}"
