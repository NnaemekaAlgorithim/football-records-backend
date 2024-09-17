from uuid import uuid4
from django.db import models
from .base_model import BaseModel
from datetime import date

class Player(BaseModel):
    """Represents a player for a MySQL database.

    Attributes:
        player_id (UUIDField): The player's unique identifier.
        first_name (CharField): The player's first name.
        last_name (CharField): The player's last name.
        height (FloatField): The player's height in meters.
        date_of_birth (DateField): The player's date of birth.
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
    date_of_birth = models.DateField(null=True, blank=True)

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

    def calculate_age(self):
        """Calculate and return the player's age based on date_of_birth."""
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
