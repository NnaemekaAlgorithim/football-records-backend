from uuid import uuid4
from django.db import models
from .base_model import BaseModel

class TeamStats(BaseModel):
    """Represents team statistics for a MySQL database.
    
    Attributes:
        team_stat_id (UUIDField): The statistics ID (primary key).
        season (CharField): The season the statistics were recorded.
        team_name (ForeignKey): The name of the team (foreign key).
        team_logo (ForeignKey): The logo of the team (foreign key).
        number_of_goals (IntegerField): Number of goals scored by the team.
        number_of_wins (IntegerField): Number of wins by the team.
        number_of_loses (IntegerField): Number of losses by the team.
        number_of_matches_played (IntegerField): Number of matches played by the team.
        possession (FloatField): Possession percentage (nullable).
        total_number_of_passes (IntegerField): Total number of passes made by the team.
    """
    team_stat_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    season = models.CharField(max_length=128)
    team_name = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='team_stats')
    team_logo = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='team_logo_stats')
    number_of_goals = models.IntegerField(default=0)
    number_of_wins = models.IntegerField(default=0)
    number_of_loses = models.IntegerField(default=0)
    number_of_matches_played = models.IntegerField(default=0)
    possession = models.FloatField(null=True, blank=True)
    total_number_of_passes = models.IntegerField(default=0)

    def __str__(self):
        return f"Stats for {self.team_name.team_name} in {self.season}"
