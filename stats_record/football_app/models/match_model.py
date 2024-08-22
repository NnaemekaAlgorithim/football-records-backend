from uuid import uuid4
from django.db import models
from .base_model import BaseModel

class Match(BaseModel):
    """Represents a match for a MySQL database.

    Attributes:
        match_id (UUIDField): The match's unique identifier.
        season (ForeignKey): The season to which the match belongs.
        league (ForeignKey): The league to which the match belongs.
        home_team (ForeignKey): The team playing at home.
        away_team (ForeignKey): The team playing away.
        match_date (DateTimeField): The date and time of the match.
        venue (CharField): The venue where the match will take place.
        home_team_score (IntegerField): The score of the home team.
        away_team_score (IntegerField): The score of the away team.
        status (CharField): The status of the match (e.g., scheduled, completed).
        match_type (CharField): The type of match (e.g., league, knockout).
    """
    match_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    season = models.ForeignKey('Season', on_delete=models.CASCADE, related_name='matches')
    league = models.ForeignKey('League', on_delete=models.CASCADE, related_name='matches')
    home_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='away_matches')
    match_date = models.DateTimeField()
    venue = models.CharField(max_length=255)
    home_team_score = models.IntegerField(null=True, blank=True)
    away_team_score = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, default='scheduled')

    MATCH_TYPE_CHOICES = [
        ('league', 'League'),
        ('knockout', 'Knockout'),
        ('friendly', 'Friendly'),
        ('group_stage', 'Group_stage'),
        ('semi_final', 'Semi_final'),
        ('quater_final', 'Quater_final'),
        ('final', 'Final'),
    ]
    match_type = models.CharField(max_length=20, choices=MATCH_TYPE_CHOICES, default='league')

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.match_date.strftime('%Y-%m-%d')}"
