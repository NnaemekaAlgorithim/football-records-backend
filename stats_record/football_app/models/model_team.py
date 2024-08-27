from uuid import uuid4
from django.db import models
from .base_model import BaseModel

class Team(BaseModel):
    """Represents a team for a MySQL database.

    Attributes:
        team_id (UUIDField): The team's ID.
        team_name (CharField): The team's name.
        team_logo (ImageField): The team's logo path.
        manager_name (CharField): The team's manager name.
        league (ForeignKey): The league in which the team competes.
    """
    team_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    team_name = models.CharField(max_length=128, unique=True)
    team_logo = models.ImageField(upload_to='team_logos/', null=True, blank=True)
    manager_name = models.CharField(max_length=128, null=True)
    league = models.ForeignKey('League', on_delete=models.CASCADE, related_name='teams_list', null=True)

    def __str__(self):
        return f"{self.team_name} - {self.league.name if self.league else 'No League'}"
