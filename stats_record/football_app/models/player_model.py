from uuid import uuid4
from django.db import models
from .base_model import BaseModel

class Player(BaseModel):
    """Represents a player for a MySQL database.

    Attributes:
        player_id (UUIDField): The player's unique identifier.
        first_name (CharField): The player's first name.
        last_name (CharField): The player's last name.
        height (FloatField): The player's height in meters.
        age (IntegerField): The player's age.
        team (ForeignKey): The team to which the player belongs.
        league (ForeignKey): The league to which the player belongs.
        primary_position (CharField): The player's primary position on the field.
        is_subscribed (BooleanField): Indicates if the player is subscribed to something.
        player_image (ImageField): The player's image path.
    """
    player_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    height = models.FloatField(help_text="Height in meters")
    age = models.IntegerField()

    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='players')
    league = models.ForeignKey('League', on_delete=models.CASCADE, related_name='players')

    PRIMARY_POSITION_CHOICES = [
        ('GK', 'Goalkeeper'),
        ('DEF', 'Defender'),
        ('MID', 'Midfielder'),
        ('FWD', 'Forward'),
    ]
    primary_position = models.CharField(max_length=10, choices=PRIMARY_POSITION_CHOICES)

    is_subscribed = models.BooleanField(default=False)
    player_image = models.ImageField(upload_to='player_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.primary_position})"
