from uuid import uuid4
from django.db import models
from .base_model import BaseModel

class League(BaseModel):
    """Represents a league for a MySQL database.

    Attributes:
        league_id (UUIDField): The league's ID.
        name (CharField): The league's name.
        country (CharField): The country the league is based in.
        founded_year (IntegerField): The year the league was founded.
        logo (ImageField): The league's logo path.
        teams (ManyToManyField): The teams participating in the league.
    """
    league_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=128, unique=True)
    country = models.CharField(max_length=128)
    founded_year = models.IntegerField()
    logo = models.ImageField(upload_to='league_logos/', null=True, blank=True)
    teams = models.ManyToManyField('Team', related_name='leagues', blank=True)

    def __str__(self):
        return self.name
