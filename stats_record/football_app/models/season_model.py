from uuid import uuid4
from django.db import models
from .base_model import BaseModel

class Season(BaseModel):
    """Represents a season for a MySQL database.

    Attributes:
        season_id (UUIDField): The season's ID.
        league (ForeignKey): The league to which the season belongs.
        year (CharField): The year or range of the season (e.g., 2023/2024).
        start_date (DateField): The start date of the season.
        end_date (DateField): The end date of the season.
        is_current (BooleanField): Indicates if this is the current season.
    """
    season_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    league = models.ForeignKey('League', on_delete=models.CASCADE, related_name='seasons')
    year = models.CharField(max_length=9)  # Example: "2023/2024"
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.league.name} - {self.year}"
