from uuid import uuid4
from django.db import models
from django.conf import settings
from .base_model import BaseModel

class TeamStats(BaseModel):
    """Represents team statistics for a MySQL database.
    
    Attributes:
        team_stat_id (UUIDField): The statistics ID (primary key).
        season (CharField): The season the statistics were recorded.
        team_name (ForeignKey): The name of the team (foreign key).
        team_logo (ForeignKey): The logo of the team (foreign key).
        opposing_team_name (CharField): The name of the opposing team.
        match_outcome (CharField): Indicates the outcome of the match.
        match_goals (IntegerField): Indicates the number of goals for a particular match. 
        match_concided_goals (IntegerField): Indicates the number of conceded goals for the match.
        match_possession (FloatField): Indicates the possession for the match.
        total_number_of_goals (IntegerField): Number of goals scored by the team.
        total_number_of_wins (IntegerField): Number of wins by the team.
        total_number_of_loses (IntegerField): Number of losses by the team.
        total_number_of_draws (IntegerField): Number of draws by the team.
        total_number_of_matches_played (IntegerField): Number of matches played by the team.
        total_number_of_passes (IntegerField): Total number of passes made by the team.
        players (ManyToManyField): List of players in the team when the match was played.
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
    season = models.CharField(max_length=128)
    team_name = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='team_stats')
    team_logo = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='team_logo_stats')
    opposing_team_name = models.CharField(null=True, max_length=128)
    match_outcome = models.CharField(max_length=4, choices=MATCH_OUTCOME_CHOICES, default=DRAW)
    match_goals = models.IntegerField(default=0)
    match_concided_goals = models.IntegerField(default=0)
    match_possession = models.FloatField(null=True, blank=True)
    total_number_of_goals = models.IntegerField(default=0)
    total_number_of_wins = models.IntegerField(default=0)
    total_number_of_loses = models.IntegerField(default=0)
    total_number_of_draws = models.IntegerField(default=0)
    total_number_of_matches_played = models.IntegerField(default=0)
    total_number_of_passes = models.IntegerField(default=0)
    players = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='team_stats_players')

    def __str__(self):
        return f"Stats for {self.team_name.team_name} in {self.season}"
